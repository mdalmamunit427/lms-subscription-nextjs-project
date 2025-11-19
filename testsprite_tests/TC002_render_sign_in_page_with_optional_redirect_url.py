import requests

BASE_URL = "http://localhost:3000"
TIMEOUT = 30


def test_render_sign_in_page_with_optional_redirect_url():
    session = requests.Session()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "python-requests/test"
    }

    # Test 1: GET /sign-in without redirect_url parameter
    try:
        response = session.get(f"{BASE_URL}/sign-in", headers=headers, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        content = response.text.lower()
        # Basic checks that sign-in page content includes Clerk sign-in indication and custom styling classes (common Tailwind css classes heuristic)
        assert "sign in" in content or "signin" in content, "Sign-in indication missing in response content"
        assert "tailwind" in content or "class=" in content, "Custom styling classes likely missing in response content"
    except requests.RequestException as e:
        assert False, f"Request to /sign-in failed: {e}"

    # Test 2: GET /sign-in with redirect_url parameter
    redirect_url = "/dashboard"
    params = {"redirect_url": redirect_url}
    try:
        response = session.get(f"{BASE_URL}/sign-in", headers=headers, params=params, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        content = response.text.lower()
        # Same content validations
        assert "sign in" in content or "signin" in content, "Sign-in indication missing in response content with redirect_url"
        assert "tailwind" in content or "class=" in content, "Custom styling classes likely missing in response content with redirect_url"
        # Verify the presence of redirect_url in the page content, usually as a hidden input or part of the script
        assert redirect_url.lower() in content, "redirect_url parameter not found in response content"
    except requests.RequestException as e:
        assert False, f"Request to /sign-in with redirect_url failed: {e}"


test_render_sign_in_page_with_optional_redirect_url()