import json
import asyncio
from functools import reduce
from urllib.parse import urljoin

import m3u8
import nest_asyncio
from aiohttp import ClientSession
from lxml.html import fromstring

nest_asyncio.apply()


class NicoVideo(object):
    def __init__(self, session: ClientSession, proxy=None) -> None:
        self.session = session
        self.proxy = proxy

    async def __aenter__(self):
        return self

    async def __aexit__(self,  *args):
        await self.session.close()

    def _build_download_session(self, e):
        def build_src_ids(e):
            def convert_to_hls_abr(e, t):
                return {
                    'src_id_to_mux': {
                        'video_src_ids': e.copy(),
                        'audio_src_ids': t.copy()
                    }
                }

            if e.get('http_parameters') and e['http_parameters'].get('use_hls_abr'):
                return reduce(lambda n, r: n + convert_to_hls_abr(r, e['audios']), e['videos'], [])
            else:
                return [convert_to_hls_abr(e['videos'], e['audios'])]

        def build_protocol(segment_duration=6 * 1000):
            return {
                "http_parameters": {
                    "parameters": {
                        "hls_parameters": {
                            "use_well_known_port": "yes",
                            "use_ssl": "yes",
                            "transfer_preset": "",
                            "segment_duration": segment_duration
                        }
                    }
                }
            }

        return {
            'recipe_id': e['recipeId'],
            'content_id': e['contentId'],
            'content_type': 'movie',
            'content_src_id_sets': [{
                'content_src_ids': build_src_ids(e)
            }],
            'timing_constraint': 'unlimited',
            'keep_method': {
                'heartbeat': {
                    'lifetime': e['heartbeatLifetime']
                }
            },
            'protocol': {
                'name': e.get('protocol', 'http'),
                'parameters': build_protocol()
            },
            'content_uri': '',
            'session_operation_auth': {
                'session_operation_auth_by_signature': {
                    'token': e['token'],
                    'signature': e['signature']
                }
            },
            'content_auth': {
                'auth_type': e.get('authType', 'ht2'),
                'max_content_count': e.get('maxContentCount', 3),
                'content_key_timeout': e.get('contentKeyTimeout', 600000),
                'service_id': 'nicovideo',
                'service_user_id': e['serviceUserId']
            },
            'client_info': {
                'player_id': e['playerId']
            },
            'priority': e['priority']
        }

    async def get_api_data(self, sm: str):
        if not sm.startswith('sm'):
            sm = 'sm' + sm

        url = f'https://www.nicovideo.jp/watch/{sm}'

        async with self.session.get(url, proxy=self.proxy) as resp:
            html = await resp.text()

        selector = fromstring(html)
        api_data = selector.xpath(
            '//*[@id="js-initial-watch-data"]/@data-api-data')

        if not api_data:
            print(html)
            return

        api_data = json.loads(api_data[0])

        return self._build_download_session(api_data['media']['delivery']['movie']['session'])

    async def fetch_video(self, sm):
        url = 'https://api.dmc.nico/api/sessions?_format=json'
        body = {'session': await self.get_api_data(sm)}

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Host': 'api.dmc.nico',
            'Origin': 'https://www.nicovideo.jp',
            'Referer': 'https://www.nicovideo.jp/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        async with self.session.post(url, json=body, headers=headers, proxy=self.proxy) as resp:
            return await resp.json()

    async def get_playlists_url(self, session_dict: dict) -> dict:
        master_m3u8_url = session_dict['content_uri']

        base_url = master_m3u8_url[:master_m3u8_url.rfind('/') + 1]

        async with self.session.get(master_m3u8_url, proxy=self.proxy) as resp:
            playlists = m3u8.parse(await resp.text()).get('playlists', None)

        if not playlists:
            raise IndexError('Playlist not found.')

        return {
            'playlists_url': list(map(lambda pl: urljoin(base_url, pl['uri']), playlists)),
            'base_url': base_url
        }

    async def get_segments_url(self, session_dict: dict):
        playlist_dict = await self.get_playlists_url(session_dict)
        playlists_url, base_url = playlist_dict['playlists_url'], playlist_dict['base_url']

        async with self.session.get(playlists_url[0], proxy=self.proxy) as resp:
            parsed_m3u8 = m3u8.parse(await resp.text())

        media_sequence = parsed_m3u8['media_sequence']

        for seg in parsed_m3u8['segments']:
            print(''.join([base_url, f'{media_sequence}/ts/', seg['uri']]))


async def main():
    proxy = 'http://127.0.0.1:10809'

    async with ClientSession() as session:
        async with NicoVideo(session, proxy=proxy) as nv:
            video_data = await nv.fetch_video('sm34322784')
            session_data = video_data['data']['session']
            print(await nv.get_segments_url(session_data))

if __name__ == '__main__':
    asyncio.run(main())
