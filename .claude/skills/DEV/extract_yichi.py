import pandas as pd

df = pd.read_csv(r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv')

print('='*80)
print('🏢 宝山区咖啡厅/空间 - 详细店铺信息提取')
print('='*80)

# 一尺花园相关
print('\n【一尺花园系列】\n')
yichi_posts = df[
    df['title'].str.contains('一尺花园', na=False) |
    df['desc'].str.contains('一尺花园', na=False)
]

for idx, row in yichi_posts.head(5).iterrows():
    title = row.get('title', '')
    desc = str(row.get('desc', ''))[:300]
    liked = row.get('liked_count', 0)

    print(f'📍 {title}')
    print(f'👍 {liked} 赞')
    print(f'📝 {desc}...')

    # 提取店铺名
    if '定海神针' in desc:
        print('✅ 店铺: 一尺花园（定海神针店）')
    if '滨江' in desc or '观光塔' in desc:
        print('✅ 位置: 宝山滨江观光塔')
    if '三层' in desc or'空间大' in desc:
        print('✅ 特点: 三层大空间')
    print('-'*80)

# 淞沪铁路/智慧湾相关
print('\n【淞沪铁路/智慧湾文创园】\n')
railway_posts = df[
    df['title'].str.contains('淞沪|铁路|智慧湾|文创', na=False) |
    df['desc'].str.contains('淞沪|铁路|智慧湾|文创', na=False)
]

for idx, row in railway_posts.head(5).iterrows():
    title = row.get('title', '')
    liked = row.get('liked_count', 0)
    desc = str(row.get('desc', ''))[:200]

    print(f'🚂 {title}')
    print(f'👍 {liked} 赞')
    print(f'📝 {desc}...')
    print('-'*80)

# 提取其他具体店名
print('\n【其他宝山区域咖啡厅】\n')

keywords = ['宝山咖啡', '顾村', '杨行', '吴淞', '宝杨路', '友谊路', '上海大学']
other_posts = []

for idx, row in df.iterrows():
    text = row['title'] + ' ' + str(row.get('desc', ''))
    for kw in keywords:
        if kw in text and '一尺花园' not in text:
            other_posts.append({
                'title': row['title'],
                'liked': row.get('liked_count', 0),
                'desc': str(row.get('desc', ''))[:150]
            })
            break

# 去重并排序
seen = set()
unique_posts = []
for post in other_posts:
    if post['title'] not in seen:
        seen.add(post['title'])
        unique_posts.append(post)

unique_posts.sort(key=lambda x: x['liked'], reverse=True)

for post in unique_posts[:10]:
    print(f'☕ {post["title"]}')
    print(f'👍 {post["liked"]} 赞')
    print(f'📝 {post["desc"]}...')
    print('-'*80)
