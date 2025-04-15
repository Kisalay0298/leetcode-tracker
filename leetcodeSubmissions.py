
import requests

# ------------------------------------------
from bs4 import BeautifulSoup
import html

def get_clean_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()
    return html.unescape(text)

# ------------------------------------------

from dotenv import load_dotenv
import os

load_dotenv()

# ------------------------------------------



USERNAME = os.getenv("USERNAME")
LIMIT = 1
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": os.getenv("REFERER"),
    "Cookie": os.getenv("COOKIE", "X_CSRFTOKEN"),
    "x-csrftoken": os.getenv("X_CSRFTOKEN")
}



def get_question_info(title_slug):
    url = "https://leetcode.com/graphql/"
    payload = {
        "query": """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            title
            difficulty
            content
            exampleTestcases
          }
        }
        """,
        "variables": {"titleSlug": title_slug}
    }
    r = requests.post(url, json=payload, headers=HEADERS)
    if r.status_code != 200:
        print(f"[!] Failed to fetch problem info for: {title_slug}")
        return None

    data = r.json()
    if "errors" in data:
        print("GraphQL Error:", data["errors"])
        return None

    return data["data"]["question"]




def get_submissions():
    url = "https://leetcode.com/graphql/"
    payload = {
        "query": """
        query submissionList($offset: Int!, $limit: Int!) {
          submissionList(offset: $offset, limit: $limit) {
            submissions {
              id
              title
              titleSlug
              timestamp
            }
          }
        }
        """,
        "variables": {"offset": 0, "limit": LIMIT}
    }
    r = requests.post(url, json=payload, headers=HEADERS)
    if r.status_code != 200:
        print(f"[!] Error fetching submissions: {r.status_code}")
        print(r.text)
        return []
    return r.json()["data"]["submissionList"]["submissions"]



def get_code(submission_id):
    url = "https://leetcode.com/graphql/"
    payload = {
        "query": """
        query submissionDetails($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
            lang {
              name
            }
          }
        }
        """,
        "variables": {"submissionId": submission_id}
    }
    r = requests.post(url, json=payload, headers=HEADERS)
    print("Status Code:", r.status_code)

    if r.status_code != 200:
        print(f"[!] Failed to fetch code for submission {submission_id}")
        return None

    response = r.json()
    if "errors" in response:
        print("GraphQL Error:", response["errors"])
        return None

    return response["data"]["submissionDetails"]


submissions = get_submissions()
if submissions is None:
    print("[!] No submissions fetched.")
else:
  for s in submissions:
      code_data = get_code(s["id"])
      problem_data = get_question_info(s["titleSlug"])

      print(f"\n=== {s['title']} ===")
      if problem_data:
          print(f"Difficulty: {problem_data['difficulty']}")
          print(f"Example Testcases:\n{problem_data['exampleTestcases']}")
          # print("\nQuestion Description:\n")
          # print(problem_data['content'])  # <- This will print HTML!
          print("\nQuestion Description:\n")
          print(get_clean_text(problem_data['content']))
      if code_data:
          print(f"Language: {code_data['lang']['name']}\nCode:\n{code_data['code']}")
      else:
          print("[!] Could not retrieve code.")











# https://leetcode-stats-api.herokuapp.com/Kisalay2767
# https://leetcode-stats-api.herokuapp.com/Kisalay2767/submissions
# https://leetcode.com/graphql/
# https://leetcode.com/graphql/  query submissionDetails($submissionId: Int!) {
#   submissionDetails(submissionId: $submissionId) {
#     code
#     lang {
#       name
#     }
#   }
