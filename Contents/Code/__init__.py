import re, string

MSNBC_PREFIX      = "/video/msnbc"
MSNBC_NAMESPACE   = {'v':'http://www.w3.org/2005/Atom', 'media':'http://search.yahoo.com/mrss/'}
MSNBC_URL         = 'http://rss.msnbc.msn.com/id/'

CACHE_INTERVAL = 3600

ART = 'art-default.jpg'
ICON = 'icon-default.jpg'

###################################################################################################
def Start():
  Plugin.AddPrefixHandler(MSNBC_PREFIX, MainMenu, 'MSNBC', ICON,ART)
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'MSNBC'
  MediaContainer.content = 'Items'
  MediaContainer.viewGroup = 'List'
  MediaContainer.art = R(ART)
  DirectoryItem.thumb = R(ICON)
  
  HTTP.CacheTime = CACHE_INTERVAL

###################################################################################################
def MainMenu():
  dir = MediaContainer()
  dir.Append(Function(DirectoryItem(News,           title="All News")))
#  dir.Append(Function(DirectoryItem(Countdown,      title="Countdown with Keith Olbermann", thumb=R('countdown.png')))) # he'll be on the Current TV plugin soon enough
  dir.Append(Function(DirectoryItem(Maddow,         title="The Rachel Maddow Show", thumb=R('maddow.png'))))
  dir.Append(Function(DirectoryItem(Nightly_News,   title="Nightly News with Brian Williams", thumb=R('nightly_news.png'))))
  dir.Append(Function(DirectoryItem(Meet_The_Press, title="Meet The Press", thumb=R('meet_the_press.png'))))
  dir.Append(Function(DirectoryItem(Today,          title="Today Show", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(Morning_Joe,    title="Morning Joe", thumb=R('joe.png'))))
  dir.Append(Function(DirectoryItem(Dateline,       title="Dateline", thumb=R('dateline.jpeg'))))
  dir.Append(Function(DirectoryItem(ZeitGeist,      title="ZeitGeist", thumb=R('zeitgeist.png'))))
  dir.Append(Function(DirectoryItem(Hardball,       title="Hardball", thumb=R('hardball.jpeg'))))
  dir.Append(Function(DirectoryItem(GetVideosRSS,   title="The Ed Show"), name=MSNBC_URL + '30012522/device/rss/vp/3096434/rss.xml', title2='The Ed Show'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,   title="Way Too Early"), name=MSNBC_URL + '32178079/device/rss/vp/3096434/rss.xml', title2='Way Too Early'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,   title="Daily Rundown"), name=MSNBC_URL + '34419168/device/rss/vp/3096434/rss.xml', title2='Daily Rundown'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,   title="MSNBC TV"), name=MSNBC_URL + '18424721/device/rss/vp/3096434/rss.xml', title2='MSNBC TV'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,   title="Andrea Mitchell Reports"), name=MSNBC_URL + '34510812/device/rss/vp/3096434/rss.xml', title2='Andrea Mitchell Reports'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,   title="The Dylan Ratigan Show"), name=MSNBC_URL + '34419165/device/rss/vp/3096434/rss.xml', title2='The Dylan Ratigan Show'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,   title="The Last Word"), name=MSNBC_URL + '38865210/device/rss/vp/3096434/rss.xml', title2='The Last Word'))
  return dir

###################################################################################################
def StripTags(str):
  return re.sub(r'<[^<>]+>', '', str)

def GetThumb(path):
  try:
    image = HTTP.Request(path, cacheTime=CACHE_1MONTH).content
    return DataObject(image, 'image/jpeg')
  except:
    return R(ICON)

def GetVideo(sender, episodeid):
  path = "http://www.msnbc.msn.com/default.cdnx/id/%s/displaymode/1157?t=.flv"%episodeid
  return Redirect(path)

def GetLatestEpisode(sender, path):
  return Redirect(XML.ElementFromURL('http://podcastfeeds.nbcnews.com/audio/podcast/%s.xml'%path).xpath('//enclosure')[0].get('url'))

###################################################################################################
def GetVideosRSS(sender, name, title2):
  dir = MediaContainer(viewGroup='Details', title2=title2)
  for video in XML.ElementFromURL(name, errors="ignore").xpath('//item', namespaces=MSNBC_NAMESPACE):
    if video.find('link').text.startswith('http://ads') == False :
      title = video.find('title').text
      episodeid = video.find('link').text.split('#')[1]
    
      if title.count("Presented By:") > 0:
        continue
      date = Datetime.ParseDate(video.find('pubDate').text).strftime('%a %b %d, %Y')
      try:
        thumbpath = video.xpath('media:content', namespaces=MSNBC_NAMESPACE)[0].get('url')
      except:
        thumbpath = ''

      summary = StripTags(video.find('description').text)

      dir.Append(Function(VideoItem(GetVideo, title=title[7:], subtitle=date, summary=summary, thumb=Function(GetThumb, path = thumbpath)),episodeid = episodeid))

  if (len(dir) == 0):
    return MessageContainer("Empty Category","This category does not contain any video.")
  else:
    return dir
  
########################### END Keith Olbermann END ################################################
########################### Rachel Maddow ##########################################################
def Maddow(sender):
  dir = MediaContainer(title2='The Rachel Maddow Show')
  dir.Append(Function(VideoItem(GetLatestEpisode,     title='Latest Full Episode', thumb=R('maddow.png')),path = 'MSNBC-MADDOW-NETCAST-M4V'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Programs", thumb=R('maddow.png')), name=MSNBC_URL + '27668917/device/rss/vp/26315908', title2='Latest Programs'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Most Viewed", thumb=R('maddow.png')), name=MSNBC_URL + '27108530/device/rss/vp/26315908', title2='Most Viewed'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Ms. Information", thumb=R('maddow.png')), name=MSNBC_URL + '26776800/device/rss/vp/26315908', title2='Ms. Information'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="GOP in Exile", thumb=R('maddow.png')), name=MSNBC_URL + '28937296/device/rss/vp/26315908', title2='GOP in Exile'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Rachel Re:", thumb=R('maddow.png')), name=MSNBC_URL + '26776790/device/rss/vp/26315908', title2='Rachel Re:'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Just Enough", thumb=R('maddow.png')), name=MSNBC_URL + '26776791/device/rss/vp/26315908', title2='Just Enough'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Recommended", thumb=R('maddow.png')), name=MSNBC_URL + '27351114/device/rss/vp/26315908', title2='Recommended'))
  return dir
  
########################### END Rachel Maddow END ##################################################
########################### Nighly News ############################################################
def Nightly_News(sender):
  dir = MediaContainer(title2='Nightly News with Brian Williams')
  dir.Append(Function(VideoItem(GetLatestEpisode,     title='Latest Full Episode', thumb=R('nightly_news.png')),path = 'MSNBC-NN-NETCAST-M4V'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Full Episodes", thumb=R('nightly_news.png')), name=MSNBC_URL + '18424748/device/rss', title2='Full Episodes'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Program", thumb=R('nightly_news.png')), name=MSNBC_URL + '22422632/device/rss', title2='Latest Program'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Most Viewed", thumb=R('nightly_news.png')), name=MSNBC_URL + '22453546/device/rss', title2='Most Viewed'))
  dir.Append(Function(DirectoryItem(NN_Web,           title="Web Only", thumb=R('nightly_news.png'))))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Brian Williams", thumb=R('nightly_news.png')), name=MSNBC_URL + '21437648/device/rss', title2='Brian Williams'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Politics", thumb=R('nightly_news.png')), name=MSNBC_URL + '21677453/device/rss', title2='Politics'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Hard Times", thumb=R('nightly_news.png')), name=MSNBC_URL + '24856627/device/rss', title2='Hard Times'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Health", thumb=R('nightly_news.png')), name=MSNBC_URL + '22827958/device/rss', title2='Health'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="World News", thumb=R('nightly_news.png')), name=MSNBC_URL + '22827879/device/rss', title2='World News'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Weather", thumb=R('nightly_news.png')), name=MSNBC_URL + '26676833/device/rss', title2='Weather'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Our Planet", thumb=R('nightly_news.png')), name=MSNBC_URL + '21437577/device/rss', title2='Our Planet'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Making a Difference", thumb=R('nightly_news.png')), name=MSNBC_URL + '21437535/device/rss', title2='Making a Difference'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="In Their Own Words", thumb=R('nightly_news.png')), name=MSNBC_URL + '21437630/device/rss', title2='In Their Own Words'))
  return dir
  
def NN_Web(sender):
  dir = MediaContainer(title2='Web Only')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('nightly_news.png')), name=MSNBC_URL + '22316432/device/rss', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Extended Interviews", thumb=R('nightly_news.png')), name=MSNBC_URL + '22423188/device/rss', title2='Extended Interviews'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="NBC Behind the Scenes", thumb=R('nightly_news.png')), name=MSNBC_URL + '23018885/device/rss', title2='NBC Behind the Scenes'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Digital Dispach", thumb=R('nightly_news.png')), name=MSNBC_URL + '21550471/device/rss', title2='Digital Dispach'))
  return dir
  
########################### END Nightly News END ###################################################
########################### Meet the Press #########################################################
def Meet_The_Press(sender):
  dir = MediaContainer(title2='Meet the Press')
  dir.Append(Function(VideoItem(GetLatestEpisode,     title='Latest Full Episode', thumb=R('meet_the_press.png')),path = 'MSNBC-MTP-NETCAST-M4V'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Full Episodes", thumb=R('meet_the_press.png')), name=MSNBC_URL + '18424745/device/rss', title2='Full Episodes'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('meet_the_press.png')), name='http://pheedo.msnbc.msn.com/id/18424744/device/rss/', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Insights & Analysis", thumb=R('meet_the_press.png')), name=MSNBC_URL + '21437686/device/rss', title2='Insights & Analysis'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="News Makers", thumb=R('meet_the_press.png')), name=MSNBC_URL + '21437662/device/rss', title2='News Makers'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Take Two", thumb=R('meet_the_press.png')), name=MSNBC_URL + '21437717/device/rss', title2='Take Two'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Meet The Candidates", thumb=R('meet_the_press.png')), name=MSNBC_URL + '21437695/device/rss', title2='Meet The Candidates'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="60th Anniversary", thumb=R('meet_the_press.png')), name=MSNBC_URL + '22410986/device/rss', title2='60th Anniversary'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Russert Remembered", thumb=R('meet_the_press.png')), name=MSNBC_URL + '25146060/device/rss', title2='Meet The Candidates'))
  return dir
  
########################### END Meet the Press END ##################################################
########################### Today Show ##############################################################
def Today(sender):
  dir = MediaContainer(title2='Today Show')
  dir.Append(Function(DirectoryItem(TS_Latest,        title="Latest Program", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Most Viewed", thumb=R('today.png')), name=MSNBC_URL + '18424824/device/rss/vp/26184891', title2='Most Viewed'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Previously", thumb=R('today.png')), name=MSNBC_URL + '26411480/device/rss/vp/26184891', title2='Previously'))
  dir.Append(Function(DirectoryItem(TS_News,          title="News", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(TS_Concert,       title="Concert Series", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(TS_Diet,          title="Diet & Health", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(TS_Entertainment, title="Entertainment", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(TS_Fashion,       title="Fashion", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Food & Wine", thumb=R('today.png')), name=MSNBC_URL + '21658719/device/rss/vp/26184891', title2='Food & Wine'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Home & Garden", thumb=R('today.png')), name=MSNBC_URL + '21658803/device/rss/vp/26184891', title2='Home & Garden'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Money", thumb=R('today.png')), name=MSNBC_URL + '23152698/device/rss/vp/26184891', title2='Money'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Parenting", thumb=R('today.png')), name=MSNBC_URL + '21658914/device/rss/vp/26184891', title2='Parenting'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Favorite People: 2008", thumb=R('today.png')), name=MSNBC_URL + '28357213/device/rss/vp/26184891', title2='Favorite People: 2008'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Pets", thumb=R('today.png')), name=MSNBC_URL + '23152689/device/rss/vp/26184891', title2='Pets'))
  dir.Append(Function(DirectoryItem(TS_Relationships, title="Relationships", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="People", thumb=R('today.png')), name=MSNBC_URL + '29411569/device/rss/vp/26184891', title2='People'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Tech & Gadgets", thumb=R('today.png')), name=MSNBC_URL + '23152694/device/rss/vp/26184891', title2='Tech & Gadgets'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Travel", thumb=R('today.png')), name=MSNBC_URL + '22828279/device/rss/vp/26184891', title2='Travel'))
  dir.Append(Function(DirectoryItem(TS_Special,       title="Special Series", thumb=R('today.png'))))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Web-only", thumb=R('today.png')), name=MSNBC_URL + '21658973/device/rss/vp/26184891', title2='Web-only'))
  return dir
  
def TS_Latest(sender):
  dir = MediaContainer(title2='Latest Program')
  dir.Append(Function(VideoItem(GetLatestEpisode,     title='Latest Full Episode', thumb=R('today.png')),path = 'MSNBC-TDY-PODCAST-M4V'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('today.png')), name=MSNBC_URL + '18424824/device/rss/vp/26184891', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Honda & Cathy Lee", thumb=R('today.png')), name=MSNBC_URL + '26316687/device/rss/vp/26184891', title2='Honda & Cathy Lee'))
  return dir
  
def TS_News(sender):
  dir = MediaContainer(title2='News')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('today.png')), name=MSNBC_URL + '22828010/device/rss/vp/26184891', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Politics", thumb=R('today.png')), name=MSNBC_URL + '25274211/device/rss/vp/26184891', title2='Politics'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Tales of Survival", thumb=R('today.png')), name=MSNBC_URL + '26316706/device/rss/vp/26184891', title2='Tales of Survival'))
  return dir

def TS_Concert(sender):
  dir = MediaContainer(title2='Concert Series')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('today.png')), name=MSNBC_URL + '21659048/device/rss/vp/26184891', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Backstage Pass", thumb=R('today.png')), name=MSNBC_URL + '25723585/device/rss/vp/26184891', title2='Backstage Pass'))
  return dir
  
def TS_Diet(sender):
  dir = MediaContainer(title2='Diet & Health')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('today.png')), name=MSNBC_URL + '22828130/device/rss/vp/26184891', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Nutrition with Joy Bauer", thumb=R('today.png')), name=MSNBC_URL + '25887307/device/rss/vp/26184891', title2='Nutrition with Joy Bauer'))
  return dir
  
def TS_Entertainment(sender):
  dir = MediaContainer(title2='Entertainment')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('today.png')), name=MSNBC_URL + '21658676/device/rss/vp/26184891', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Critics Class", thumb=R('today.png')), name=MSNBC_URL + '26316665/device/rss/vp/26184891', title2='Critics Class'))
  return dir

def TS_Fashion(sender):
  dir = MediaContainer(title2='Fashion')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('today.png')), name=MSNBC_URL + '21658676/device/rss/vp/26184891', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Ambush Makeovers", thumb=R('today.png')), name=MSNBC_URL + '25887326/device/rss/vp/26184891', title2='Ambush Makeovers'))
  return dir
  
def TS_Relationships(sender):
  dir = MediaContainer(title2='Fashion')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('today.png')), name=MSNBC_URL + '21658957/device/rss/vp/26184891', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Wedding", thumb=R('today.png')), name=MSNBC_URL + '21659067/device/rss/vp/26184891', title2='Wedding'))
  return dir
  
def TS_Special(sender):
  dir = MediaContainer(title2='Special Series')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Anchor Roots", thumb=R('today.png')), name=MSNBC_URL + '26408377/device/rss/vp/26184891', title2='Anchor Roots'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Where in the World", thumb=R('today.png')), name=MSNBC_URL + '21659089/device/rss/vp/26184891', title2='Where in the World'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Today in Beijing", thumb=R('today.png')), name=MSNBC_URL + '25854156/device/rss/vp/26184891', title2='Today in Beijing'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Ends of the Earth", thumb=R('today.png')), name=MSNBC_URL + '21636851/device/rss/vp/26184891', title2='Ends of the Earth'))
  return dir
  
########################### END Today Show END #####################################################
########################### Morning Joe ############################################################
def Morning_Joe(sender):
  dir = MediaContainer(title2='Morning Joe')
  dir.Append(Function(VideoItem(GetLatestEpisode,     title='Latest Full Episode', thumb=R('joe.png')),path = 'MSNBC-SCARBOROUGH-NETCAST-M4V'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Most Viewed", thumb=R('joe.png')), name=MSNBC_URL + '28184433/device/rss/vp/28159725', title2='Most Viewed'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Politics", thumb=R('joe.png')), name=MSNBC_URL + '28184154/device/rss/vp/28159725', title2='Politics'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="News You Can't Use", thumb=R('joe.png')), name=MSNBC_URL + '28184451/device/rss/vp/28159725', title2="News You Can't Use"))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Economy", thumb=R('joe.png')), name=MSNBC_URL + '28184592/device/rss/vp/28159725', title2='Economy'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Health Care", thumb=R('joe.png')), name=MSNBC_URL + '30314086/device/rss/vp/28159725', title2='Health Care'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Scoop", thumb=R('joe.png')), name=MSNBC_URL + '28184387/device/rss/vp/28159725', title2='Scoop'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Best of Morning Joe", thumb=R('joe.png')), name=MSNBC_URL + '28117873/device/rss/vp/28159725', title2='Best of Morning Joe'))
  return dir
  
########################### END Morning Joe END #####################################################
########################### ZeitGeist ###############################################################
def ZeitGeist(sender):
  dir = MediaContainer(title2='ZeitGeist')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('zeitgeist.png')), name=MSNBC_URL + '20418176/device/rss/vp/26852192', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Most Viewed", thumb=R('zeitgeist.png')), name=MSNBC_URL + '27707215/device/rss/vp/26852192', title2='Most Viewed'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Willie on TV", thumb=R('zeitgeist.png')), name=MSNBC_URL + '25196846/device/rss/vp/26852192', title2='Willie on TV'))
  return dir
  
########################### END ZeitGeist END #######################################################
########################### Hardball ################################################################
def Hardball(sender):
  dir = MediaContainer(title2='Hardball')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('hardball.jpeg')), name=MSNBC_URL + '29058318/device/rss/vp/29279101', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Most Viewed", thumb=R('hardball.jpeg')), name=MSNBC_URL + '29058303/device/rss/vp/29279101', title2='Most Viewed'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Newsmakers", thumb=R('hardball.jpeg')), name=MSNBC_URL + '29058145/device/rss/vp/29279101', title2='Newsmakers'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Politics Fix", thumb=R('hardball.jpeg')), name=MSNBC_URL + '29058233/device/rss/vp/29279101', title2='Politics Fix'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Slideshow", thumb=R('hardball.jpeg')), name=MSNBC_URL + '29058266/device/rss/vp/29279101', title2='Slideshow'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Big Number", thumb=R('hardball.jpeg')), name=MSNBC_URL + '29058274/device/rss/vp/29279101', title2='Big Number'))
  return dir
  
########################### END Hardball END ########################################################
########################### Dateline ################################################################
def Dateline(sender):
  dir = MediaContainer(title2='Dateline')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('dateline.jpeg')), name='http://pheedo.msnbc.msn.com/id/18424719/device/rss/', title2='Latest Clips'))
  return dir
  
########################### END Dateline END ########################################################
########################### Dateline ################################################################
def edshow(sender):
  dir = MediaContainer(title2='The Ed Show')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips", thumb=R('edshow.jpeg')), name='http://pheedo.msnbc.msn.com/id/18424719/device/rss/', title2='Latest Clips'))
  return dir
  
########################### END Dateline END ########################################################
########################### All News ################################################################
def News(sender):
  dir = MediaContainer(title2='All News')
  dir.Append(Function(DirectoryItem(N_US,             title="U.S. News")))
  dir.Append(Function(DirectoryItem(N_World,          title="World news")))
  dir.Append(Function(DirectoryItem(N_Business,       title="Business")))
  dir.Append(Function(DirectoryItem(N_Politics,       title="Politics")))
  dir.Append(Function(DirectoryItem(N_Entertainment,  title="Entertainment")))
  dir.Append(Function(DirectoryItem(N_Health,         title="Health")))
  dir.Append(Function(DirectoryItem(N_Sports,         title="Sports")))
  dir.Append(Function(DirectoryItem(N_Tech,           title="Tech & Science")))
  dir.Append(Function(DirectoryItem(N_Travel,         title="Travel")))
  dir.Append(Function(DirectoryItem(N_Weather,        title="Weather")))
  return dir
  
def N_US(sender):
  dir = MediaContainer(title2='U.S. News')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name='http://pheedo.msnbc.msn.com/id/21426262/device/rss', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="The Elkhart Project"), name=MSNBC_URL + '29637267/device/rss', title2='The Elkhart Project'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Crime & Courts"), name=MSNBC_URL + '21427653/device/rss', title2='Crime & Courts'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Life"), name=MSNBC_URL + '21427662/device/rss', title2='Life'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Environment"), name=MSNBC_URL + '21427657/device/rss', title2='Environment'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Faith"), name=MSNBC_URL + '23600340/device/rss', title2='Faith'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Education"), name=MSNBC_URL + '23600346/device/rss', title2='Education'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Race & Ethnicity"), name=MSNBC_URL + '21427673/device/rss', title2='Race & Ethnicity'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Military"), name=MSNBC_URL + '21427669/device/rss', title2='Military'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Security"), name=MSNBC_URL + '21427678/device/rss', title2='Security'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Weird News"), name='http://pheedo.msnbc.msn.com/id/18424731/device/rss', title2='Weird news'))
  dir.Append(Function(DirectoryItem(N_Weather,        title="Weather")))
  return dir

def N_World(sender):
  dir = MediaContainer(title2='World News')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name='http://pheedo.msnbc.msn.com/id/21426473/device/rss/', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Americas"), name=MSNBC_URL + '21427766/device/rss', title2='Americas'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Africa"), name=MSNBC_URL + '21427760/device/rss', title2='Africs'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Asia-Pacific"), name=MSNBC_URL + '21427768/device/rss', title2='Asia-Pacific'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Conflict in Iraq"), name=MSNBC_URL + '21427754/device/rss', title2='Conflict in Iraq'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Europe"), name=MSNBC_URL + '21427850/device/rss', title2='Europe'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="South & Central Asia"), name=MSNBC_URL + '21427861/device/rss', title2='South & Central Asia'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Middle East & N. Africa"), name=MSNBC_URL + '21427857/device/rss', title2='Middle East & N. Africa'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Terrorism"), name=MSNBC_URL + '21427756/device/rss', title2='Terrorism'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Wonderful World"), name=MSNBC_URL + '21427651/device/rss', title2='Wonderful World'))
  return dir

def N_Business(sender):
  dir = MediaContainer(title2='Business')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name='http://pheedo.msnbc.msn.com/id/18424694/device/rss/', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Stock and Economy"), name=MSNBC_URL + '21427890/device/rss', title2='Stocks and Economy'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="U.S. Business"), name=MSNBC_URL + '21427903/device/rss', title2='U.S. Business'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Autos"), name=MSNBC_URL + '21427924/device/rss', title2='Autos'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Real Estate"), name=MSNBC_URL + '21427971/device/rss', title2='Real Estate'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Retail"), name=MSNBC_URL + '21427996/device/rss', title2='Retail'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Careers"), name=MSNBC_URL + '21427991/device/rss', title2='Careers'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Personal Finance"), name=MSNBC_URL + '21427918/device/rss', title2='Personal Finance'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Small Business"), name=MSNBC_URL + '21427920/device/rss', title2='Small Business'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Your Business"), name=MSNBC_URL + '18424833/device/rss', title2='Your Business'))
  return dir

def N_Politics(sender):
  dir = MediaContainer(title2='Politics')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name='http://pheedo.msnbc.msn.com/id/18424734/device/rss/', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="The White House"), name=MSNBC_URL + '21427723/device/rss', title2='The White House'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Capitol Hill"), name=MSNBC_URL + '21427731/device/rss', title2='Capitol Hill'))
  dir.Append(Function(DirectoryItem(Morning_Joe,      title="Morning Joe", thumb=R('joe.png'))))
  dir.Append(Function(DirectoryItem(Hardball,         title="Hardball", thumb=R('hardball.jpeg'))))
  dir.Append(Function(DirectoryItem(Meet_The_Press,   title="Meet The Press", thumb=R('meet_the_press.png'))))
  return dir

def N_Entertainment(sender):
  dir = MediaContainer(title2='Entertainment')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name='http://pheedo.msnbc.msn.com/id/18424692/device/rss/', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Scoop", thumb=R('joe.png')), name=MSNBC_URL + '28184387/device/rss/vp/28159725', title2='Scoop'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Celebrities"), name=MSNBC_URL + '21428100/device/rss', title2='Celebrities'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Television"), name=MSNBC_URL + '21428108/device/rss', title2='Television'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Movies"), name=MSNBC_URL + '18424697/device/rss', title2='Movies'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Music"), name=MSNBC_URL + '21428116/device/rss', title2='Music'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Lifestyle"), name=MSNBC_URL + '21428119/device/rss', title2='Lifestyle'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Access Hollywood"), name=MSNBC_URL + '20418142/device/rss', title2='Access Hollywoody'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Keeping Tabs"), name=MSNBC_URL + '20498047/device/rss', title2='Keeping Tabs'))
  return dir

def N_Health(sender):
  dir = MediaContainer(title2='Health')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name='http://pheedo.msnbc.msn.com/id/21427299/device/rss/', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Diet & Nutrition"), name=MSNBC_URL + '21428136/device/rss', title2='Diet & Nutrition'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Women's Health"), name=MSNBC_URL + '21428143/device/rss', title2="Women's Health"))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Men's Health"), name=MSNBC_URL + '21428151/device/rss', title2="Men's Health"))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Kids & Parenting"), name=MSNBC_URL + '21428155/device/rss', title2='Kids & Parenting'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Health Care"), name=MSNBC_URL + '30018753/device/rss', title2='Health Care'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Food Safety"), name=MSNBC_URL + '30018791/device/rss', title2='Food Safety'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Sexual Health"), name=MSNBC_URL + '21428170/device/rss', title2='Sexual Health'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Pet Health"), name=MSNBC_URL + '21428208/device/rss', title2='Pet Health'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Fitness"), name=MSNBC_URL + '21428178/device/rss', title2='Fitness'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Heart Health"), name=MSNBC_URL + '21428183/device/rss', title2='Heart Health'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Mental Health"), name=MSNBC_URL + '21428162/device/rss', title2='Mental Health'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Cancer"), name=MSNBC_URL + '21428191/device/rss', title2='Cancer'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Aging"), name=MSNBC_URL + '21428203/device/rss', title2='Aging'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Skin & Beauty"), name=MSNBC_URL + '21480182/device/rss', title2='Skin & Beauty'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Animal Tracks"), name=MSNBC_URL + '18424682/device/rss', title2='Animal Tracks'))
  return dir

def N_Sports(sender):
  dir = MediaContainer(title2='Sports')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Sports"), name='http://pheedo.msnbc.msn.com/id/21426493/device/rss/', title2='Latest Sports'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="NFL"), name='http://nbcsports.msnbc.com/id/21428022/device/rss', title2='NFL'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Baseball"), name='http://nbcsports.msnbc.com/id/21428015/device/rss', title2='Baseball'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="NCAA Hoops"), name='http://nbcsports.msnbc.com/id/21428068/device/rss', title2='NCAA Hoops'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="NBA"), name='http://nbcsports.msnbc.com/id/21428039/device/rss', title2='NBA'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Golf"), name='http://nbcsports.msnbc.com/id/21428026/device/rss', title2='Golf'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="NHL"), name='http://nbcsports.msnbc.com/id/21428025/device/rss', title2='NHL'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="MMA"), name='http://nbcsports.msnbc.com/id/21428080/device/rss', title2='MMA'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="NCAA Football"), name='http://nbcsports.msnbc.com/id/21428047/device/rss', title2='NCAA Football'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Horse Racing"), name='http://nbcsports.msnbc.com/id/21428075/device/rss', title2='Horse Racing'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="NASCAR/Motors"), name='http://nbcsports.msnbc.com/id/22114938/device/rss', title2='NASCAR/Motors'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Tennis"), name='http://nbcsports.msnbc.com/id/21428033/device/rss', title2='Tennis'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Sports Oddities"), name='http://nbcsports.msnbc.com/id/23017283/device/rss', title2='Sports Oddities'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Mad Dog Minute"), name='http://nbcsports.msnbc.com/id/23017809/device/rss', title2='Mad Dog Minute'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Matty Blake"), name='http://nbcsports.msnbc.com/id/23258082/device/rss', title2='Matty Blake'))
  return dir

def N_Tech(sender):
  dir = MediaContainer(title2='Tech')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name='http://pheedo.msnbc.msn.com/id/18424747/device/rss/', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Space"), name=MSNBC_URL + '18424741/device/rss', title2='Space'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Science"), name=MSNBC_URL + '21428316/device/rss', title2='Science'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Technology"), name=MSNBC_URL + '21428240/device/rss', title2='Technology'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Games"), name=MSNBC_URL + '26560891/device/rss', title2='Games'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Red Tape Chronicals"), name=MSNBC_URL + '28780760/device/rss', title2='Red Tape Chronicals'))
  return dir

def N_Travel(sender):
  dir = MediaContainer(title2='Travel')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name='http://pheedo.msnbc.msn.com/id/21427411/device/rss/', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Travel Tips"), name=MSNBC_URL + '26560980/device/rss', title2='Travel Tips'))
  return dir

def N_Weather(sender):
  dir = MediaContainer(title2='Weather')
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Latest Clips"), name=MSNBC_URL + '25198763/device/rss', title2='Latest Clips'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="National Forecasts"), name=MSNBC_URL + '30331543/device/rss', title2='National Forecasts'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Regional Forecasts"), name=MSNBC_URL + '30331544/device/rss', title2='Regional Forecasts'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Top Local Forecasts"), name=MSNBC_URL + '30331545/device/rss', title2='Top Local Forecasts'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Vacation Forecasts"), name=MSNBC_URL + '30331546/device/rss', title2='Vacation Forecasts'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Forecast Earth"), name=MSNBC_URL + '30331549/device/rss', title2='Forecast Earth'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Epic Conditions"), name=MSNBC_URL + '30332550/device/rss', title2='Epic Conditions'))
  dir.Append(Function(DirectoryItem(GetVideosRSS,     title="Weather Changed History"), name=MSNBC_URL + '30331551/device/rss', title2='Weather Changed History'))
  return dir

########################### END All News END #####################################################

