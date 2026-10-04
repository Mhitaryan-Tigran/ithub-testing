import allure
import httpx

from settings import settings


class HTTPClient(httpx.Client):
    @allure.step("GET {url}")
    def get(self, url, **kwargs):
        return super().get(url, **kwargs)

    @allure.step("POST {url}")
    def post(self, url, **kwargs):
        return super().post(url, **kwargs)

    @allure.step("PUT {url}")
    def put(self, url, **kwargs):
        return super().put(url, **kwargs)

    @allure.step("DELETE {url}")
    def delete(self, url, **kwargs):
        return super().delete(url, **kwargs)


def attach_response(response):
    allure.attach(f"{response.request.method} {response.request.url}\n\n{response.request.content.decode() or '—'}", "request", allure.attachment_type.TEXT)
    allure.attach(response.text, f"response {response.status_code}", allure.attachment_type.JSON)


def get_http_client():
    return HTTPClient(base_url=settings.base_url, timeout=settings.timeout, headers={"api_key": settings.api_key}, event_hooks={"response": [lambda r: r.read() and attach_response(r)]})
