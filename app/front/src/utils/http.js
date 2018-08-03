import { baseUrl, versions } from '../app-config'

/**
 * 解析资源定位参数
 *
 * @param {any} router
 * @param {any} resourceParams
 * @returns
 */
function parseResource (router, resourceParams) {
  let _router = router
  let _params = resourceParams

  if (_params === null) return _router

  for (let [, value] of _params) {
    (value !== undefined) && (_router = `${_router}/${value}`)
  }

  return _router
};

/**
 * 解析查询参数
 *
 * @param {any} url
 * @param {any} query
 */
function parseQuery (url, query) {
  if (query === undefined) return url

  url += '?'

  for (let p in query) {
    url += `${p}=${query[p]}&`
  }

  return url.slice(0, -1)
}

/**
 * 解析返回状态
 *
 * @param {any} res 返回数据
 * @param {any} type 是否需要通讯拦截去绑定手机号
 *                   0：需要拦截；1：不需要拦截
 * @returns
 */
function parseResult (res, type) {
  return new Promise((resolve, reject) => {
    switch (res.statusCode) {
      case 200:
      case 204:
        resolve()
        break
      case 500:
        reject(res)
        let code = res.data.code
        if (code && type !== 1) {
          switch (code) {
            case 10001:
              break
          }
        }
        break
      default:
        reject(res)
        break
    }
  })
};

/**
 * 生成通讯头配置
 *
 * @param {string} type string 通讯的类型
 * @param {object} header object 外部传入的通讯头部配置
 * @returns
 */
function getHeader (type, header) {
  return new Promise((resolve) => {
    let newHeader = {}

    switch (type) {
      case 'GET':
        newHeader['content-type'] = 'application/x-www-form-urlencoded'
        break
      default:
        newHeader['content-type'] = 'application/json'
        break
    }

    if (header && (header.Authorization === null)) {
      resolve({ ...newHeader, ...header })
    } else {
      let getUserToken = require('./user-info').getUserToken
      getUserToken().then(token => {
        newHeader['Authorization'] = token
      }).finally(() => {
        resolve({ ...newHeader, ...header })
      })
    }
  })
}

const HTTP_POOL = []
const MAX_HTTP_COUNT = 10
let nowHttpCount = 0

/**
 * 执行通讯
 *
 * @param {string} method 通讯的类型
 */
function request (method, {
  router,
  type,
  header,
  query,
  data,
  resource
}) {
  return new Promise((resolve, reject) => {
    getHeader(method, header).then(header => {
      let url = parseResource(`${baseUrl}/v${versions}/${router}`, resource)
      query && (url = parseQuery(url, query))

      let obj = {
        url,
        method,
        data,
        header,
        success (res) {
          parseResult(res, type).then(
            () => (resolve(res.data)),
            () => (reject(res))
          )
        },
        fail (res) {
          console.log('通讯失败', res)
          reject(res)
        },
        complete () {
          if (HTTP_POOL.length > 0) {
            HTTP_POOL.shift()()
          } else {
            nowHttpCount--
          }
        }
      }

      if (method === 'PUT') {
        obj.data = {
          data
        }
      }

      if (nowHttpCount >= MAX_HTTP_COUNT) {
        HTTP_POOL.push(() => {
          wx.request(obj)
        })
      } else {
        nowHttpCount++
        wx.request(obj)
      }
    })
  })
}

let http = {
  /**
     * 发起PUT请求
     *
     * @param {object} options - 通讯配置
     * @param {string} options.router - 路由地址
     * @param {object} options.data - 请求数据
     * @param {Map} options.resource - 资源定位参数
     */
  put ({
    router,
    config: {
      type = 0
    } = {
      type: 0
    },
    config: {
      header = null
    } = {
      header: null
    },
    data = null,
    resource = null
  }) {
    return request('PUT', {
      router,
      type,
      header,
      data,
      resource
    })
  },
  /**
     * 发起GET请求
     *
     * @param {object} options - 通讯配置
     * @param {string} options.router - 路由地址
     * @param {object} options.data - 请求数据
     * @param {Map} options.resource - 资源定位参数
     * @param {object} options.query - 查询参数
     */
  get ({
    router,
    config: {
      type = 0
    } = {
      type: 0
    },
    config: {
      header = null
    } = {
      header: null
    },
    query = {},
    resource = null
  }) {
    return request('GET', {
      router,
      type,
      header,
      data: query,
      resource
    })
  },
  /**
     * 发起POST请求
     *
     * @param {object} options - 通讯配置
     * @param {string} options.router - 路由地址
     * @param {object} options.data - 请求数据
     * @param {Map} options.resource - 资源定位参数
     * @param {object} options.query - 查询参数
     * @param {object} options.header - 自定义头部
     */
  post ({
    router,
    config: {
      type = 0
    } = {
      type: 0
    },
    config: {
      header = null
    } = {
      header: null
    },
    data = null,
    resource = null,
    query = null
  }) {
    return request('POST', {
      router,
      type,
      header,
      data,
      resource,
      query
    })
  },
  /**
     * 发起DELETE请求
     *
     * @param {object} options - 通讯配置
     * @param {string} options.router - 路由地址
     * @param {object} options.data - 请求数据
     * @param {Map} options.resource - 资源定位参数
     * @param {object} options.query - 查询参数
     */
  delete ({
    router,
    config: {
      type = 0
    } = {
      type: 0
    },
    config: {
      header = null
    } = {
      header: null
    },
    data = null,
    resource = null,
    query = null
  }) {
    return request('DELETE', {
      router,
      type,
      header,
      data,
      resource,
      query
    })
  }
}

export default http
