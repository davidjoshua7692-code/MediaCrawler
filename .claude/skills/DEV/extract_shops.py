import pandas as pd
import re

# 读取数据
df = pd.read_csv('d:\\MediaCrawler-main\\data\\xhs\\csv\\search_contents_2026-01-20.csv')

print('='*80)
print('📍 宝山区咖啡厅/办公空间 - 具体店名提取')
print('='*80)

# 提取标题和描述
all_titles = []
for idx, row in df.iterrows():
    title = str(row.get('title', ''))
    desc = str(row.get('desc', ''))
    liked = row.get('liked_count', 0)
    note_id = row.get('note_id', '')

    all_titles.append({
        'title': title,
        'desc': desc,
        'liked': liked,
        'note_id': note_id
    })

# 按点赞排序
all_titles.sort(key=lambda x: x['liked'], reverse=True)

print('\n🔥 TOP 20 高互动帖子（按点赞数）\n')
for i, post in enumerate(all_titles[:20], 1):
    print(f"{i}. {post['title'][:70]}")
    print(f"   👍 {post['liked']} 赞")
    # 提取可能的地名
    text = post['title'] + ' ' + post['desc']
    locations = re.findall(r'(宝山|淞沪|铁路|园区|上海大学|吴淞|杨行|顾村|智慧湾|文创)', text)
    if locations:
        print(f"   📍 关键词: {', '.join(set(locations))}")
    print()

print('='*80)
print('🏢 提及的具体店名/品牌\n')

# 品牌识别
brands = {
    '一尺花园': [],
    '星巴克': [],
    'M STAND': [],
    '瑞幸': [],
    'Manner': [],
    'Costa': [],
}

for post in all_titles[:50]:  # 只看前50个
    text = post['title'] + ' ' + post['desc']

    for brand in brands.keys():
        if brand.lower() in text.lower() or brand.replace(' ', '') in text:
            brands[brand].append(post['title'][:60])

for brand, titles in brands.items():
    if titles:
        print(f'☕ {brand}: {len(titles)}条')
        for title in titles[:2]:
            print(f'   - {title}')
        print()

print('='*80)
print('🗺️ 宝山区具体地点提及\n')

# 详细地点提取
locations = {
    '淞沪铁路/文创园': 0,
    '智慧湾': 0,
    '上海大学': 0,
    '吴淞': 0,
    '杨行': 0,
    '顾村': 0,
    '宝杨路': 0,
    '友谊路': 0,
}

for post in all_titles:
    text = post['title'] + ' ' + post['desc']

    for loc in locations.keys():
        if loc in text or loc.replace('/', '') in text:
            locations[loc] += 1

# 排序显示
sorted_locs = sorted(locations.items(), key=lambda x: x[1], reverse=True)
for loc, count in sorted_locs:
    if count > 0:
        print(f'{loc}: {count}次')
