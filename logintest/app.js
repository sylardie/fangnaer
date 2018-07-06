//app.js
App({
  onLaunch: function () {
    //调用API从本地缓存中获取数据
    var jwt = wx.getStorageSync('jwt');
    var that = this;
    if (!jwt.access_token) { //检查 jwt 是否存在 如果不存在调用登录
      that.login();
    } else {
      console.log(jwt.account_id);
    }
  },
  login: function () {
    // 登录部分代码
    var that = this;
    wx.login({
      // 调用 login 获取 code
      success: function (res) {
        var code = res.code;
        wx.getUserInfo({
          // 调用 getUserInfo 获取 encryptedData 和 iv
          success: function (res) {
            console.log('8888', res)
            // success
            that.globalData.userInfo = res.userInfo;
            var encryptedData = res.encryptedData || 'encry';
            var iv = res.iv || 'iv';
            wx.request({ // 发送请求 获取 jwt
              url: 'http://127.0.0.1:8000' + '/api-token-auth/?code=' + code,
              header: {
                Authorization: ''
              },
              data: {
                username: res.userInfo.nickName,
                password: '123456',
                grant_type: "password",
                auth_approach: 'wxapp',
              },
              method: "POST",
              success: function (res) {
                if (res.statusCode === 201) {
                  // 得到 jwt 后存储到 storage，
                  wx.showToast({
                    title: '登录成功',
                    icon: 'success'
                  });
                  wx.setStorage({
                    key: "jwt",
                    data: res.data
                  });
                  that.globalData.access_token = res.data.access_token;
                  that.globalData.account_id = res.data.sub;
                } else if (res.statusCode === 400) {
                  // 如果没有注册调用注册接口
                  that.register();
                } else {
                  // 提示错误信息
                  wx.showToast({
                    title: res.data.text,
                    icon: 'success',
                    duration: 2000
                  });
                }
              },
              fail: function (res) {
                console.log('request token fail');
              }
            })
          },
          fail: function () {
            // fail
          },
          complete: function () {
            // complete
          }
        })
      }
    })

  },
  register: function () {
    // 注册代码
    var that = this;
    wx.login({ // 调用登录接口获取 code
      success: function (res) {
        var code = res.code;
        wx.getUserInfo({
          // 调用 getUserInfo 获取 encryptedData 和 iv
          success: function (res) {
            // success
            that.globalData.userInfo = res.userInfo;
            var encryptedData = res.encryptedData || 'encry';
            var iv = res.iv || 'iv';
            console.log(iv);
            wx.request({ // 请求注册用户接口
              url: 'http://127.0.0.1:8000' + '/wechat/login/',
              header: {
                Authorization: ''
              },
              data: {
                encryptedData: encryptedData,
                iv: iv,
                code: code,
              },
              method: "POST",
              success: function (res) {
                console.log('7777', res)
                if (res.statusCode === 200) {
                  wx.showToast({
                    title: '注册成功',
                    icon: 'success'
                  });
                  that.login();
                } else if (res.statusCode === 400) {
                  wx.showToast({
                    title: '用户已注册',
                    icon: 'success'
                  });
                  that.login();
                } else if (res.statusCode === 403) {
                  wx.showToast({
                    title: res.data.text,
                    icon: 'success'
                  });
                }
                console.log(res.statusCode);
                console.log('request token success');
              },
              fail: function (res) {
                console.log('request token fail');
              }
            })
          },
          fail: function () {
            // fail
          },
          complete: function () {
            // complete
          }
        })
      }
    })

  },

  get_user_info: function (jwt) {
    wx.request({
      url: 'http://127.0.0.1:8000' + '/auth/accounts/self',
      header: {
        Authorization: jwt.token_type + ' ' + jwt.access_token
      },
      method: "GET",
      success: function (res) {
        if (res.statusCode === 201) {
          wx.showToast({
            title: '已注册',
            icon: 'success'
          });
        } else if (res.statusCode === 401 || res.statusCode === 403) {
          wx.showToast({
            title: '未注册',
            icon: 'error'
          });
        }

        console.log(res.statusCode);
        console.log('request token success');
      },
      fail: function (res) {
        console.log('request token fail');
      }
    })
  },

  globalData: {
    userInfo: null
  }
})