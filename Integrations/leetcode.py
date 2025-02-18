import requests
from fastapi import FastAPI, HTTPException

def leetcode_description(title_slug):
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
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() 
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"LeetCode API error: {str(e)}")
    
#Function for fetching problem from id
def leetcode_problem(frontend_id):
    try:
        problems_response = requests.get("https://leetcode.com/api/problems/algorithms/")
        problems_data = problems_response.json()

        target_problem = None
        for problem in problems_data['stat_status_pairs']:
            if problem['stat']['frontend_question_id'] == frontend_id:
                target_problem = problem
                break
    
        if not target_problem:
            raise HTTPException(status_code=404, detail="Problem not found")
    
        title_slug = target_problem['stat']['question__title_slug']
        result = leetcode_description(title_slug)
        
        if isinstance(result, str):  
            raise HTTPException(status_code=500, detail=result)
            
        return result  

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))