import wepy from 'wepy'
import http from './http'

/**
 * 获取用户token
 *
 * @param {any} params
 * @returns
 */
function getUserToken () {
  return new Promise((resolve) => {
    registerUser().then(res => resolve(res._token))
  })
}

let registerUserPromise = null

/**
 * 注册用户
 */
function registerUser () {
  if (registerUserPromise !== null) {
    return registerUserPromise
  }

  registerUserPromise = new Promise((resolve) => {
    wepy.login().then(res => {
      http.post({
        router: 'login/',
        data: {
          code: res.code
        },
        config: {
          header: { Authorization: null }
        }
      }).then((res) => {
        resolve(res)
      })
    }).catch(err => {
      console.error(err)
    })
  })

  return registerUserPromise
}

export {
  registerUser,
  getUserToken
}
