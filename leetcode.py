import requests
import json

def get_question_description(title_slug):
    url = "https://leetcode.com/graphql"
    
  
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            content
            difficulty
            topicTags {
                name
            }
        }
    }
    """
    

    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"
    }

    body = {
        "query": query,
        "variables": {
            "titleSlug": title_slug
        }
    }
    
 
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"

def get_problem_by_frontend_id_and_description(frontend_id):
    problems_response = requests.get("https://leetcode.com/api/problems/algorithms/")
    problems_data = problems_response.json()
    

    target_problem = None
    for problem in problems_data['stat_status_pairs']:
        if problem['stat']['frontend_question_id'] == frontend_id:
            target_problem = problem
            break
    
    if not target_problem:
        return "Problem not found"
    
    
    title_slug = target_problem['stat']['question__title_slug']
    
    
    return get_question_description(title_slug)


result = get_problem_by_frontend_id_and_description(208)
print(json.dumps(result, indent=2))