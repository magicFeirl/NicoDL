function buildProtocol(e) {
  return {
    "http_parameters": {
      "parameters": {
        "hls_parameters": {
          "use_well_known_port": "yes",
          "use_ssl": "yes",
          "transfer_preset": "",
          "segment_duration": 6000
        }
      }
    }
  }
}

function buildSrcIds(e) {
  return e.http_parameters && e.http_parameters.use_hls_abr ? e.videos.reduce((function (n, r, i, o) {
    return n.concat(t(o.slice(-(o.length - i)), e.audios))
  }

  ), []) : [t(e.videos, e.audios)];

  function t(e, t) {
    return {
      src_id_to_mux: {
        video_src_ids: e.concat(),
        audio_src_ids: t.concat()
      }
    }
  }
}

const buildDownloadSession = (e) => {
  // 没有用 HLSABR
  return {
    recipe_id: e.recipeId,
    content_id: e.contentId,
    content_type: "movie",
    content_src_id_sets: [{
      content_src_ids: buildSrcIds(e)
    }],
    timing_constraint: "unlimited",
    keep_method: {
      heartbeat: {
        lifetime: e.heartbeatLifetime
      }
    },
    protocol: {
      name: e.protocol || 'http',
      parameters: buildProtocol(e)
    },
    content_uri: "",
    session_operation_auth: {
      session_operation_auth_by_signature: {
        token: e.token,
        signature: e.signature
      }
    },
    content_auth: {
      auth_type: e.authType || 'ht2',
      max_content_count: e.maxContentCount,
      content_key_timeout: e.contentKeyTimeout,
      service_id: "nicovideo",
      service_user_id: e.serviceUserId
    },
    client_info: {
      player_id: e.playerId
    },
    priority: e.priority
  }
}

const watchData = document.querySelector('#js-initial-watch-data').dataset
const apiData = JSON.parse(watchData.apiData)
const envData = JSON.parse(watchData.environment)

const session = buildDownloadSession(apiData['media']['delivery']['movie']['session'])

fetch("https://api.dmc.nico/api/sessions?_format=json", {
  "headers": {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json",
  },
  "referrer": "https://www.nicovideo.jp/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": JSON.stringify({ session: session }),
  "method": "POST",
  "mode": "cors",
  "credentials": "omit"
});