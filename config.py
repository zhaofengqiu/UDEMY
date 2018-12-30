
USERNAME = " "

PASSWORD = " "
USERID=" "
Auto = " "
URLMESDSSAGE = "https://www.udemy.com/api-2.0/users/me/subscribed-courses/course_id/lectures/video_id?fields%5Basset%5D=@min,download_urls,external_url,slide_urls,status,captions,thumbnail_url,time_estimation,thumbnail_sprite,stream_urls&fields%5Bcaption%5D=@default,is_translation&fields%5Bcourse%5D=id,url,locale&fields%5Blecture%5D=@default,course,can_give_cc_feedback,download_url"
COURSE_IDS_GET_URL="https://www.udemy.com/api-2.0/users/%s/subscribed-profile-courses/?fields[course]=@default,avg_rating_recent,rating,bestseller_badge_content,badges,content_info,discount,is_recently_published,is_wishlisted,num_published_lectures,num_reviews,num_subscribers,buyable_object_type,headline,instructional_level,objectives_summary,content_length_practice_test_questions,num_published_practice_tests,published_time,is_user_subscribed,has_closed_caption,preview_url,context_info"%(USERID)
VIDEOS_IDS_GET_URL= "https://www.udemy.com/api-2.0/courses/course_id/cached-subscriber-curriculum-items/?page_size=1400&fields[lecture]=@min,object_index,asset,supplementary_assets,sort_order,is_published,is_free&fields[quiz]=@min,object_index,title,sort_order,is_published&fields[practice]=@min,object_index,title,sort_order,is_published&fields[chapter]=@min,description,object_index,title,sort_order,is_published&fields[asset]=@min,title,filename,asset_type,external_url,length,status"
HEADERS={"Authorization":Auto,
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
BASEPATH = r" "
THREAD_NUM = 5
DOWNLOADSUMS = 1
