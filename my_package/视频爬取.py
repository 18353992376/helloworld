import requests
from bs4 import BeautifulSoup


def get_video_info(url):
    """
    合法获取视频基础信息示例
    需遵守网站的robots.txt规则及API使用条款
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 示例：解析页面中的公开信息
            title = soup.find('meta', property='og:title')['content']
            description = soup.find('meta', property='og:description')['content']

            return {
                'title': title,
                'description': description,
                'status': 'success'
            }

    except Exception as e:
        return {'error': str(e)}


# 使用示例（需替换为合法可访问的URL）
video_info = get_video_info('https://v.qq.com/x/cover/mzc00200shxravh/n4100xo6isx.html?j_vid=u4100q76725&j_cut_vid=a41005b0unt&j_is_win_vid=1')
print(video_info)

