import requests

BASE_URL = "http://localhost:3000"
TIMEOUT = 30


def test_render_sign_up_page_with_optional_redirect_url():
    url = f"{BASE_URL}/sign-up"
    headers = {
        "Accept": "text/html",
    }

    # Test without redirect_url parameter
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    try:
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        content = response.text.lower()
        # Basic checks for Clerk SignUp component indication & custom styling class presence
        assert "clerk-signup" in content or "clerk_signup" in content or "sign-up" in content, \
            "Sign-up component indicator not found in response content"
        # Check for presence of Tailwind or custom CSS classes in HTML response (example)
        assert "class=" in content, "No CSS classes found in sign-up page content"
    except AssertionError:
        print("Failed rendering sign-up page without redirect_url")
        raise

    # Test with redirect_url parameter
    redirect_url = "/"
    params = {"redirect_url": redirect_url}
    response_redirect = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
    try:
        assert response_redirect.status_code == 200, f"Expected status 200 for redirect_url test, got {response_redirect.status_code}"
        content_redirect = response_redirect.text.lower()
        assert "clerk-signup" in content_redirect or "clerk_signup" in content_redirect or "sign-up" in content_redirect, \
            "Sign-up component indicator not found with redirect_url parameter"
        # Check that the redirect_url is embedded in the page (commonly via a hidden input or script)
        assert redirect_url in content_redirect, "Redirect URL not present in sign-up page content"
    except AssertionError:
        print("Failed rendering sign-up page with redirect_url parameter")
        raise


test_render_sign_up_page_with_optional_redirect_url()