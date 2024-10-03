import requests
from bs4 import BeautifulSoup


def getArtists(songID):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'referer': f'https://music.youtube.com/watch?v={songID}',
    }

    json_data = {
        'videoId': ID,
        'isAudioOnly': True,
        'context': {
            'client': {
                'clientName': 'WEB_REMIX',
                'clientVersion': '1.20240918.01.00',
            },
        },

        'browseId': f'MPTC{songID}',

    }

    artistsJSON = requests.post(
        'https://music.youtube.com/youtubei/v1/browse',
        # params=params,
        # cookies=cookies,
        headers=headers,
        json=json_data,
    ).text
    # print(artistsJSON)
    # ).json()['onResponseReceivedActions'][0]['openPopupAction']['popup']['dismissableDialogRenderer']['sections'][0]['dismissableDialogContentSectionRenderer']['subtitle']['runs']
    # exit()

    artists = []
    for i in range(0, len(artistsJSON)):
        artist = artistsJSON[i]['text']
        if artist != '\n':
            artists.append(artist)
        # print(artistsJSON[i]['text'])

    return artists

def getUploadDate(songID):
    response = requests.get(f'https://www.youtube.com/watch?v={songID}')
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the upload date element
    upload_date = soup.find('meta', itemprop='datePublished')

    if upload_date:
        return upload_date['content'].split("T")[0]
    else:
        return ''

def getArtistJSON(artistID):
    json_data = {
        'context': {
            'client': {
                'clientName': 'WEB_REMIX',
                'clientVersion': '1.20240918.01.00',
            },
        },
        'browseId': artistID,
        # 'continuation': '4qmFsgIwEhxNUEFEVUNNdEpNV053cXRnV0Z5UDBoR3lzcTRRGhBnZ01HZWdRYUFnRUNvQVlC',
    }

    response = requests.post('https://music.youtube.com/youtubei/v1/browse',
    #     # params=params,
    #     # cookies=cookies,
    #     # headers=headers,
        json=json_data,
    )
    
    # print(response.text)
    # exit()
    return response.json()

def getAlbumSongsJSON(browseID):

    json_data = {
        'context': {
            'client': {
                'clientName': 'WEB_REMIX',
                'clientVersion': '1.20240918.01.00',
            },
        },
        'browseId': browseID,
        # 'params': 'ggMrGilPTEFLNXV5X2xsYml3V2p3bFJDNjU1NFBBSzg1RklSVDEwV3NnSVdsWQ%3D%3D',
    }

    response = requests.post(
        'https://music.youtube.com/youtubei/v1/browse',
        # params=params,
        # cookies=cookies,
        # headers=headers,
        json=json_data,
    )
    # print(response.text); exit()
    # return response.json()
    return response

def getAlbumSongs(AlbumSongsJSON, browseID):


    parentBrowseID = browseID[3]


    albums = AlbumSongsJSON['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['musicResponsiveHeaderRenderer']['title']['runs']

    albumName = albums[0]['text']


    # print(f'----------- {albumName} -----------')
    # exit()
    # albumCover = AlbumSongsJSON['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']
    
    songs = AlbumSongsJSON['contents']['twoColumnBrowseResultsRenderer']['secondaryContents']['sectionListRenderer']['contents'][0]['musicShelfRenderer']['contents']

    # Cycle album songs
    for i in range(0, len(songs)):

        songTitle = songs[i]['musicResponsiveListItemRenderer']['flexColumns'][0]['musicResponsiveListItemFlexColumnRenderer']['text']['runs'][0]['text']
        # print(songTitle)
        
        # Cycle album artists
        try:
            albumArtistsJSON = AlbumSongsJSON['contents']['twoColumnBrowseResultsRenderer']['secondaryContents']['sectionListRenderer']['contents'][1]['musicCarouselShelfRenderer']['contents'][0]['musicTwoRowItemRenderer']['subtitle']['runs'][1]['text']
            if albumArtistsJSON == ' • ':
                raise Exception()
        except:
            try:
                albumArtistsJSON = AlbumSongsJSON['contents']["twoColumnBrowseResultsRenderer"]["secondaryContents"]["sectionListRenderer"]["contents"][0]["musicShelfRenderer"]["contents"][0]["musicResponsiveListItemRenderer"]["flexColumns"][1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["run"]
            except:
                try:
                    albumArtistsJSON = AlbumSongsJSON['contents']["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicResponsiveHeaderRenderer"]["straplineTextOne"]["runs"]
                except:
                    albumArtistsJSON = []
        # print(albumArtistsJSON)
        songAlbumArtists = []
        if albumArtistsJSON != []:
            for j in range(0, len(albumArtistsJSON)):
                # print(j)
                if (albumArtistsJSON[j]['text'] != ', ') and (albumArtistsJSON[j]['text'] != ' & '):
                    songAlbumArtists.append(albumArtistsJSON[j]['text'])

        # print(albumArtistsJSON)  


        songArtists = []
        # if album has only one artist, artist array doesnt exist
        try:
            # Cycle artists
            totalArtists = songs[i]['musicResponsiveListItemRenderer']['flexColumns'][1]['musicResponsiveListItemFlexColumnRenderer']['text']['runs']
            for j in range(0, len(totalArtists)):
                if (totalArtists[j]['text'] != ', ') and (totalArtists[j]['text'] != ' & '):
                    songArtists.append(totalArtists[j]['text'])


        except:
            # if there is no artists, song artists are same as album artist
            songArtists = songAlbumArtists

        if songAlbumArtists == [] and len(songArtists) > 0:
            songAlbumArtists.append(songArtists[0])


        # exit()
        # print(len(totalArtists))


        
        songTrack = f'{i+1}/{len(songs)}'


        try:
            songID = songs[i]["musicResponsiveListItemRenderer"]["overlay"]["musicItemThumbnailOverlayRenderer"]["content"]["musicPlayButtonRenderer"]["playNavigationEndpoint"]["watchEndpoint"]["videoId"]
        except:
            # exception if any song is banned / deleted
            continue

        
        # print(str(AlbumSongsJSON.text))
        # exit()
        
        # print(f'songTitle:{songTitle} \
        #     songAlbumArtists:{songAlbumArtists} \
        #     songTrack:{songTrack} \
        #     songArtists:{songArtists} \
        #     songID:{songID} \
        #     ')

    print(f'Parent Album ID: {parentBrowseID} - Album/song: {albumName}/{songTitle}  - track:{songTrack} - disc:{browseID[0]}/{browseID[1]}')

specialAlbumsBrowseIDs = [] # used later to save specialAlbums to avoid infinite recursion

artistJSON = getArtistJSON('MPADUCvK0z8WYFw3RFcyyNbyzL9A') # fran laoren
# artistJSON = getArtistJSON('MPADUCSLbbBoUqpin6BE34whSOvA') # goofy ah albums

# get all browseIDs, there is a browseID for every album
browseIDs = artistJSON['contents']['singleColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['gridRenderer']['items']

# Cycle all browseIDs, (same as cycling all albums)
i = 0
while i < len(browseIDs): # if is not a while is not posible to append new browse IDs in a running iteration
    print(f'------------------------{i}/{len(browseIDs)}------------------------')

    try:
        # browseID of current album
        browseID = [1, 1, browseIDs[i]['musicTwoRowItemRenderer']['title']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId']]
        browseID.append(browseID[2])
    except:
        browseID = browseIDs[i] # contains [1, 3, '323vj5hof3480n7vu52h']
        
    # AlbumJSON containg all songs and more info
    AlbumSongsJSON = getAlbumSongsJSON(browseID[2])
    # ------- debug shit -------
    # print(AlbumSongsJSON.text) 
    # exit()
    AlbumSongsJSON = AlbumSongsJSON.json()


    # albums with a darker skin color (NIGGERS) 
    # print(browseID[2], specialAlbumsBrowseIDs)
    if not browseID[2] in specialAlbumsBrowseIDs: # if this iteration is an special album dont do anything to avoid infinite recursion
        skipSpecialEditions = False
        albumsSpecialEdition = False
        try:
            albumsSpecialEdition = AlbumSongsJSON['contents']['twoColumnBrowseResultsRenderer']['secondaryContents']['sectionListRenderer']['contents'][1]['musicCarouselShelfRenderer']['contents']
        except:
            skipSpecialEditions = True

        if not skipSpecialEditions:
            
            totalAlbumsSpecialEdition = len(albumsSpecialEdition)+1

            browseID[1] = totalAlbumsSpecialEdition
            print(':LEN:', totalAlbumsSpecialEdition)
            for j in range(0, len(albumsSpecialEdition)):
                # print(albumsSpecialEdition[j]['musicTwoRowItemRenderer']['title']['runs'][0]['text'])
                specialAlbumBrowseID = albumsSpecialEdition[j]['musicTwoRowItemRenderer']['title']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId']
                # print(specialAlbumsBrowseIDs)
                # print(browseIDs)
                browseIDs.append([j+2, totalAlbumsSpecialEdition, specialAlbumBrowseID, browseID[2]])
                # print([j+2, totalAlbumsSpecialEdition, specialAlbumBrowseID, browseID[2]])
                specialAlbumsBrowseIDs.append(specialAlbumBrowseID)
                # print(browseIDs)
    
    getAlbumSongs(AlbumSongsJSON, browseID)

    i += 1 # needed


    # print(len(songs))
    # exit()
    # albumCover = songs[0]['musicResponsiveHeaderRenderer']['thumbnail']['musicThumbnailRenderer']['thumbnail']['thumbnails'][3]['url']

    # print(songs)
    # exit()


    



    # exit()



    # exit()
    # print(AlbumSongsJSON['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['musicResponsiveHeaderRenderer']['title']['runs'][0]['text'])



    

# print(getArtists(ID))
# print(getUploadDate(ID))


