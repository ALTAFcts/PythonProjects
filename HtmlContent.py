import threading
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import gc
import requests
from readability import Document

def GetLinkHttpResponse(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
            allow_redirects=True
        )

        # print("Status:", response.status_code)
        # print("Final URL:", response.url)
        # print("Content-Type:", response.headers.get("Content-Type"))

        html = response.text

        # First check HTTP status
        if response.status_code >= 400:
            return {
                "success": False,
                "status": "HTTP_ERROR",
                "http_code": response.status_code,
                "content": html
            }

        # Check CAPTCHA / challenge
        captcha_result = detect_captcha(html, response.url)

        if captcha_result:
            return {
                "success": False,
                "status": "CAPTCHA",
                "http_code": response.status_code,
                "reason": captcha_result,
                "content": html
            }

        # Check bot/access blocking
        block_result = detect_block(html)

        if block_result:
            return {
                "success": False,
                "status": "BLOCKED",
                "http_code": response.status_code,
                "reason": block_result,
                "content": html
            }

        # Extract visible text
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(" ", strip=True)

        if len(text) < 100:
            return {
                "success": False,
                "status": "EMPTY",
                "http_code": response.status_code,
                "content": html
            }

        return {
            "success": True,
            "status": "SUCCESS",
            "http_code": response.status_code,
            "content": html,
            "text": text
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status": "TIMEOUT"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "status": "REQUEST_ERROR",
            "error": str(e)
        }

    except Exception as e:
        return {
            "success": False,
            "status": "ERROR",
            "error": str(e)
        }

def detect_captcha(html, url=""):
    html_lower = html.lower()

    captcha_keywords = [
        "captcha",
        "recaptcha",
        "hcaptcha",
        "cloudflare turnstile",
        "cf-chl-captcha",
        "challenge-platform",
        "verify you are human",
        "verify you're human",
        "prove you are human",
        "security check",
        "human verification",
        "are you a robot",
        "robot check"
    ]

    for keyword in captcha_keywords:
        if keyword in html_lower:
            return keyword

    return None

def detect_block(html):
    html_lower = html.lower()

    block_keywords = [
        "access denied",
        "request blocked",
        "forbidden",
        "bot detected",
        "automated access",
        "unusual traffic",
        "too many requests",
        "temporarily blocked",
        "security policy",
        "web application firewall",
        "incapsula",
        "imperva",
        "akamai bot manager",
        "perimeterx"
    ]

    for keyword in block_keywords:
        if keyword in html_lower:
            return keyword

    return None

def clean_article_html(html):

    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that normally contain no article content
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "canvas",
        "form",
        "nav",
        "footer"
    ]):
        tag.decompose()

    # -----------------------------------------
    # Find possible article containers
    # -----------------------------------------

    candidates = []

    for tag in soup.find_all([
        "article",
        "main",
        "section",
        "div"
    ]):

        text = tag.get_text(" ", strip=True)

        if len(text) < 200:
            continue

        # Count paragraph-like elements
        paragraphs = tag.find_all(["p", "h1", "h2", "h3"])

        if len(paragraphs) >= 2:

            candidates.append({
                "tag": tag,
                "text": text,
                "length": len(text),
                "paragraphs": len(paragraphs)
            })

    if not candidates:
        return ""

    # Pick the candidate with substantial textual content
    candidates.sort(
        key=lambda x: (
            x["paragraphs"],
            x["length"]
        ),
        reverse=True
    )

    article = candidates[0]["tag"]

    # -----------------------------------------
    # Extract meaningful elements
    # -----------------------------------------

    result = []

    for element in article.find_all([
        "h1",
        "h2",
        "h3",
        "p",
        "li",
        "blockquote"
    ]):

        text = element.get_text(" ", strip=True)

        if not text:
            continue

        text = re.sub(r"\s+", " ", text).strip()

        if len(text) < 3:
            continue

        result.append(text)

    # Remove duplicate lines
    final = []
    seen = set()

    for line in result:

        key = line.lower()

        if key not in seen:
            seen.add(key)
            final.append(line)

    return "\n".join(final)


