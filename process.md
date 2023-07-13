从 api-data['media']['delivery']['moive'] 拿到的数据，经过 buildDownloadSession 加工后会成为 sessions 接口的参数，**需要进一步获取到详细的传参构造方法以补全传参**。
``` javascript
const e = {"contentId": "out1", "audios": [{"id": "archive_aac_128kbps", "isAvailable": false, "metadata": {"bitrate": 128000, "samplingRate": 48000, "loudness": {"integratedLoudness": -20, "truePeak": 0.1}, "levelIndex": 1, "loudnessCollection": [{"type": "video", "value": 1}, {"type": "pureAdPreroll", "value": 0.3981071705534972}, {"type": "houseAdPreroll", "value": 0.3981071705534972}, {"type": "networkAdPreroll", "value": 0.3981071705534972}, {"type": "pureAdMidroll", "value": 0.3981071705534972}, {"type": "houseAdMidroll", "value": 0.3981071705534972}, {"type": "networkAdMidroll", "value": 0.3981071705534972}, {"type": "pureAdPostroll", "value": 0.3981071705534972}, {"type": "houseAdPostroll", "value": 0.3981071705534972}, {"type": "networkAdPostroll", "value": 0.3981071705534972}, {"type": "nicoadVideoIntroduce", "value": 0.5011872336272722}, {"type": "nicoadBillboard", "value": 1}, {"type": "marquee", "value": 0.6309573444801932}]}}, {"id": "archive_aac_64kbps", "isAvailable": true, "metadata": {"bitrate": 64000, "samplingRate": 48000, "loudness": {"integratedLoudness": -20, "truePeak": 0.1}, "levelIndex": 0, "loudnessCollection": [{"type": "video", "value": 1}, {"type": "pureAdPreroll", "value": 0.3981071705534972}, {"type": "houseAdPreroll", "value": 0.3981071705534972}, {"type": "networkAdPreroll", "value": 0.3981071705534972}, {"type": "pureAdMidroll", "value": 0.3981071705534972}, {"type": "houseAdMidroll", "value": 0.3981071705534972}, {"type": "networkAdMidroll", "value": 0.3981071705534972}, {"type": "pureAdPostroll", "value": 0.3981071705534972}, {"type": "houseAdPostroll", "value": 0.3981071705534972}, {"type": "networkAdPostroll", "value": 0.3981071705534972}, {"type": "nicoadVideoIntroduce", "value": 0.5011872336272722}, {"type": "nicoadBillboard", "value": 1}, {"type": "marquee", "value": 0.6309573444801932}]}}], "videos": [{"id": "archive_h264_600kbps_360p", "isAvailable": true, "metadata": {"label": "360p | 0.6M", "bitrate": 600000, "resolution": {"width": 640, "height": 360}, "levelIndex": 1, "recommendedHighestAudioLevelIndex": 1}}, {"id": "archive_h264_300kbps_360p", "isAvailable": true, "metadata": {"label": "360p | 0.3M", "bitrate": 300000, "resolution": {"width": 640, "height": 360}, "levelIndex": 0, "recommendedHighestAudioLevelIndex": 1}}], "session": {"recipeId": "nicovideo-sm34322784", "playerId": "nicovideo-6-bApkgHx44Q_1689170904955", "videos": ["archive_h264_600kbps_360p", "archive_h264_300kbps_360p"], "audios": ["archive_aac_64kbps"], "movies": [], "protocols": ["http", "hls"], "authTypes": {"http": "ht2", "hls": "ht2"}, "serviceUserId": "6-bApkgHx44Q_1689170904955", "token": "{\"service_id\":\"nicovideo\",\"player_id\":\"nicovideo-6-bApkgHx44Q_1689170904955\",\"recipe_id\":\"nicovideo-sm34322784\",\"service_user_id\":\"6-bApkgHx44Q_1689170904955\",\"protocols\":[{\"name\":\"http\",\"auth_type\":\"ht2\"},{\"name\":\"hls\",\"auth_type\":\"ht2\"}],\"videos\":[\"archive_h264_300kbps_360p\",\"archive_h264_600kbps_360p\"],\"audios\":[\"archive_aac_64kbps\"],\"movies\":[],\"created_time\":1689170905000,\"expire_time\":1689257305000,\"content_ids\":[\"out1\"],\"heartbeat_lifetime\":120000,\"content_key_timeout\":600000,\"priority\":0,\"transfer_presets\":[]}", "signature": "7aa9678866da2aab5a1647aaa2fb9ab0e19b7aade6d996068dc8a4b490c9b487", "contentId": "out1", "heartbeatLifetime": 120000, "contentKeyTimeout": 600000, "priority": 0, "transferPresets": [], "urls": [{"url": "https://api.dmc.nico/api/sessions", "isWellKnownPort": true, "isSsl": true}]}}

const  _buildDownloadSession = (e) => {
    return {
        recipe_id: e.recipe_id,
        content_id: e.content_id,
        content_type: "movie",
        content_src_id_sets: [{
            content_src_ids: 't(e)'
        }],
        timing_constraint: "unlimited",
        keep_method: {
            heartbeat: {
                lifetime: e.heartbeat_lifetime
            }
        },
        protocol: {
            name: e.protocol,
            parameters: 'n(e)'
        },
        content_uri: "",
        session_operation_auth: {
            session_operation_auth_by_signature: {
                token: e.token,
                signature: e.signature
            }
        },
        content_auth: {
            auth_type: e.auth_type,
            max_content_count: e.max_content_count,
            content_key_timeout: e.content_key_timeout,
            service_id: "nicovideo",
            service_user_id: e.service_user_id
        },
        client_info: {
            player_id: e.player_id
        },
        priority: e.priority
    }
}

_buildDownloadSession(e.session)
```