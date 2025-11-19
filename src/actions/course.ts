"use server";

import connectDB from "@/lib/mongodb";
import Subscription from "@/models/Subscription";

export async function activateSubscription(
    clerkId: string,
    stripePaymentIntentId: string,
    stripeCustomerId?: string
) {

    try {
        await connectDB();

        const existingByPayment = await Subscription.findOne({stripePaymentIntentId});

        if(existingByPayment) {
            return {
                success: true,
                message: 'Subscription already processed',
                subscription: JSON.parse(JSON.stringify(existingByPayment)),
                alreadyProcessed: true,
            }
        }

        let subscription = await Subscription.findOne({clerkId});
        if(subscription) {
            subscription.status = 'completed';
            subscription.activatedAt = new Date();
            subscription.stripePaymentIntentId = stripePaymentIntentId;

            if(stripeCustomerId) {
                subscription.stripeCustomerId = stripeCustomerId;
            }

            await subscription.save()
          

        } else {
            // create new subscription
            subscription = await Subscription.create({
                clerkId,
                userId: clerkId,
                status: 'completed',
                amount: 99,
                currency: 'USD',
                stripePaymentIntentId,
                stripeCustomerId,
                purchaseDate: new Date(),
                activatedAt: new Date(),
            })
        }

        return {
            success: true,
            message: 'Subscription activated',
            subscription: JSON.parse(JSON.stringify(subscription)),
            alreadyProcessed: false,
        }


    } catch (error) {
        console.error('Error activating subscription:', error);
        return {
            success: false,
            message: 'Failed activating subscription',
            error: error instanceof Error ? error.message : 'Unknown error',

        }
    }
    
}


export async function checkSubscription(clerkId:string) {
    try {
        await connectDB();

        const subscription = await Subscription.findOne({
            clerkId,
            status: 'completed',
        }).lean();
        return {
            success: true,
            isSubscribed: !!subscription,
            subscription: subscription ? JSON.parse(JSON.stringify(subscription)) : null,
        }
    } catch (error) {
        console.error('Error checking subscription:', error);
        return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
            isSubscribed: false,
            subscription: null,
        }
    }
}