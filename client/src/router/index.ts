import { createRouter, createWebHistory } from 'vue-router'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css'
import { menuStore } from '@/stores/menu'
import { getAccessToken, getRefreshToken, setToken } from '@/utils/cookies'
import { userinfoStore } from '@/stores/userinfo'
import { refreshToken } from '@/api/user' // progress bar style

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: {
        name: 'lobby'
      }
    },
    {
      path: '/login',
      name: 'login',
      // @ts-ignore
      component: () => import('@/views/UserLogin.vue')
    },
    {
      path: '/drive',
      name: 'drive',
      // @ts-ignore
      component: () => import('@/views/AliyunDrive.vue')
    },
    {
      path: '/upload',
      name: 'upload',
      // @ts-ignore
      component: () => import('@/views/FileUpload.vue')
    },
    {
      path: '/files',
      name: 'files',
      // @ts-ignore
      component: () => import('@/views/FileManager.vue')
    },
    {
      path: '/books',
      name: 'books',
      // @ts-ignore
      component: () => import('@/views/BookManager.vue')
    },
    {
      path: '/lobby',
      name: 'lobby',
      // @ts-ignore
      component: () => import('@/views/LobbyView.vue')
    },
    {
      path: '/book/:id',
      name: 'book',
      // @ts-ignore
      component: () => import('@/views/BookDetailView.vue')
    },
    {
      path: '/user',
      name: 'user',
      // @ts-ignore
      component: () => import('@/views/user/UserBase.vue'),
      children: [
        {
          path: 'info',
          name: 'userinfo',
          // @ts-ignore
          component: () => import('@/views/user/UserInfo.vue')
        },
        {
          path: 'pwd',
          name: 'password',
          // @ts-ignore
          component: () => import('@/views/user/UserPassword.vue')
        }
      ]
    }
  ]
})
const whiteList = ['/login', '/auth-redirect', '/logout'] // no redirect whitelist

router.beforeEach(async (to, from, next) => {
  NProgress.start()

  const menuList = [
    'lobby',
    'book',
    'books',
    'files',
    'drive',
    'userinfo',
    'password',
    'upload',
    'register'
  ]
  const menu = menuStore()
  if (menuList.indexOf(<string>to.name) !== -1) {
    menu.activeIndex = to.name
  }
  const accessToken = getAccessToken()

  if (to.name === 'lobby' && accessToken) {
    const store = userinfoStore()
    if (!store.username) {
      await store.getUserInfo()
    }
  }

  if (['lobby', 'register', 'book'].indexOf(<string>to.name) !== -1) {
    next()
    NProgress.done()
    return
  }

  if (accessToken) {
    if (to.path === '/login') {
      // if is logged in, redirect to the home page
      next({ path: '/' })
      NProgress.done()
    } else {
      const store = userinfoStore()
      if (store.username) {
        next()
        NProgress.done()
      } else {
        await store.getUserInfo()
        next()
        NProgress.done()
      }
    }
  } else {
    /* has no token*/
    const RefreshToken = getRefreshToken()
    if (RefreshToken) {
      const res = await refreshToken({ refresh: RefreshToken })
      setToken(res.data)
      next()
      NProgress.done()
      return
    }

    if (whiteList.indexOf(to.path) !== -1) {
      // in the free login whitelist, go directly
      next()
      NProgress.done()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

export default router
