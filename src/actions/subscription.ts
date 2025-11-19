"use server";

import { currentUser } from "@clerk/nextjs/server";
import Stripe from "stripe";
import { checkSubscription } from "./course";


const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
    apiVersion: '2025-10-29.clover'
})

export async function createCheckoutSession() {
    try {
        const user = await currentUser();

        if(!user) {
            return {
                success: false,
                error: "You must be signed in to purchase a subscription."
            }
        }

        const {isSubscribed} = await checkSubscription(user.id);

        if(isSubscribed) {
            return {
                success: false,
                error: "You already have a subscription.",
            }
        }

        const orgin = process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";

        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card'],
            mode: 'payment',
            line_items: [
                {
                    price_data: {
                        currency: 'usd',
                        product_data: {
                            name: 'All-Access Course Subscription',
                            description: 'Unlock all courses and content instantly for lifetime access',
                        },
                        unit_amount: 99 * 100
                    },
                    quantity: 1
                }
            ],
            success_url: `${process.env.NEXT_PUBLIC_APP_URL}/payment-success?session_id={CHECKOUT_SESSION_ID}`,
            cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/?canceled=true`,
            customer_email: user.emailAddresses[0].emailAddress,
            metadata: {
                clerkId: user.id,
                userEmail: user.emailAddresses[0].emailAddress,
                userName: `${user.firstName || ''} ${user.lastName || ''}`.trim()
            }
        });

        return {
            success: true,
            sessionId: session.id,
            url: session.url
        }


    } catch (error) {
        console.error("Error creating checkout session:", error);
        return {
            success: false,
            error: "An error occurred while processing your request. Please try again."
        }
    }
}