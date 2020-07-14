import os
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = os.environ.get('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def print_header(line):
  '''Format and print header block sized to length of line'''
  header_str = '='
  header_line = header_str * len(line)
  print('\n' + header_line)
  print(line)
  print(header_line)
  
def youtubeSearch(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,
        developerKey = DEVELOPER_KEY)


# The q parameter specifies the query term to search for.

    search_response = youtube.search().list( 
        q = options.q,
        part = 'id, snippet',
        maxResults= options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []


    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                        search_result['id']['videoId']))
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                        search_result['id']['channelId']))
        elif search_result['id']['kind'] =='youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                        search_result['id']['playlistsId']))

    print('Videos:\n', '\n'.join(videos), '\n')
    print('Channels:\n', '\n'.join(channels), '\n')
    print('Playlists:\n', '\n'.join(playlists), '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--q', help='Search term', default='Cats')
    parser.add_argument('--max-results', help = 'Max results', default= 25)

    args = parser.parse_args()

    try:
        youtubeSearch(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
