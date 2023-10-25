from django.urls import path
from .views import *
#import AllUserProfileView, UploadFileView, QuestionView, ParameterView, SubcriberView, SubcriberViewForUnSub
urlpatterns = [
    path('get-all-user/', AllUserProfileView.as_view(), name='all_user'),
    path('upload-file/', UploadFileView.as_view(), name='upload-file'),
    path('question/', QuestionView.as_view(), name='question'),
    path('parameter/', ParameterView.as_view(), name='parameter'),
    path('subcriber/', SubcriberView.as_view(), name='subcriber'),
    path('unsubcriber/', SubcriberViewForUnSub.as_view(), name='subcriber'),
    path('anonymous-user/', AnnonymusUserCount.as_view(), name='anonymous-user'),
    path('chart-data/', ChartDataView.as_view(), name='chart-data'),
    path('user-export-csv/', UserCSVFile.as_view(), name='user-csv'),
    path('alldata-export-csv/', DataCSVFile.as_view(), name='data-csv'),
    path('chat-history/', GetChatHistory.as_view(), name='chat-history'),
    path('get-file/', GetFileView.as_view(), name='get-file'),
    path('view-file/<int:file_id>/', GetPDFFileView.as_view(), name='view-file'),
    path('document-view/', GetDocumentView.as_view(), name='docuemnt-view'),
    path('update-profile/', UserProfileView.as_view(), name='update-profile'),
]




# def premera(url, websiteName):
#     options = Options()
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     options.headless = True
#     options.add_argument("--window-size=1280x720")
#     options.add_argument("start-maximised")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     ser = Service("selenium/chromedriver.exe")
#     driver = webdriver.Chrome(options=options, service=ser)
#     final_data = []
#     url = re.sub(r'\&paging\=.*', '', url)
#     url = re.sub(r'\&spage\=.*', '', url)
#     driver.get(url)
#     print(url)
#     print('Starting from page 1 ')
#     print('Scrapping page 1 ...')

#     print()
#     html = driver.page_source
#     soup = bs(html, 'html.parser')
#     final_data = []
#     pages_url = []
#     pages_url.append(url)
#     page = 1
#     product_count = 0
#     count = 0
#     while True:
#         print("true hai")


#         mytable =soup.find('tbody')

#         if mytable:
#             print("")
#             rows = mytable.find_all('tr')

#             # Process each row and extract data from its cells
#             for row in rows:
#                 # Find all cells (td) within the row

#                 cells = row.find_all('td')

#                 mycount = 0

#                 for cell in cells:



#                     try:


#                         mycount=mycount+1
#                         print("muc",mycount)

#                         if mycount == 2:
#                             print("result:", cell.text)

#                         # Now, if you want to extract the text content of this td element, use cell.text




#                     except:
#                         print("jaskj")


#                     try:
#                         anchor_tag = cell.find('a')



#                         if anchor_tag:
#                             # Extract the 'href' attribute from the anchor tag
#                             href_value = anchor_tag['href']
#                             final_data.append(href_value)
#                             print("href:", href_value)
#                     except:

#                         print("cell:", cell.text)



#         else:
#             print("tbody element not found in the HTML content.")
#         print("final",len(final_data))
#         break

