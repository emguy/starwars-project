<template>
  <div
    class="header"
    :class="{'test-mode':isTestMode}"
  >
    <p
      v-if="isLoadingResult"
      class="onload-message-display"
    >
      Working ...
    </p>
    <p
      v-else-if="systemMessage"
      class="onload-message-display"
    >
      {{ systemMessage }}
    </p>
    <div>
      <img
        src="@/assets/logo.svg"
        alt="ericsson logo"
        style="width:36px"
      >
    </div>
    <p class="heading">
      <router-link
        v-if="isTestMode"
        :to="'/manifest-browser-test'"
      >
        River Testing
      </router-link>
      <router-link
        v-else
        :to="'/manifest-browser'"
      >
        {{ appTitle }}
      </router-link>
    </p>
    <div
      class="menu"
      v-if="!isTestMode"
    >
      <router-link
        v-for="(item, index) in menuItems"
        :key="index"
        class="menu-item"
        :to="item.path"
      >
        {{ item.name }}
      </router-link>
    </div>
    <div class="control-area">
      <p
        class="error-message"
        :class="{active: errorMessage}"
      >
        {{ errorMessage }}
      </p>
      <div class="login-logout">
        <p v-if="isLoggedIn">
          <font-awesome-icon
            class="icon"
            icon="user-cog"
          />
          <span class="name-label">{{ appUser.displayName }}</span>
          <span
            class="usergroup-label"
            v-if="userGroupInfo"
          >
            {{ userGroupInfo.groupName }}
          </span>
          <span class="separator" />
          <font-awesome-icon
            class="icon"
            icon="sign-out-alt"
          />
          <span @click="logout">logout</span>
        </p>
        <p v-else>
          <font-awesome-icon
            class="icon"
            icon="sign-in-alt"
          />
          <span @click="login">login</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      appTitle: process.env.VUE_APP_TITLE,
      menuItems: [
        {
          name: 'Manifest Browser',
          path: '/manifest-browser'
        },
        {
          name: 'River Status',
          path: '/river-status'
        },
        {
          name: 'Import Manifest',
          path: '/manifest-importer'
        }
      ]
    }
  },
  computed: {
    isTestMode () {
      return this.$route.name.endsWith(':test')
    },
    isLoggedIn () {
      return this.$store.getters['isLoggedIn']
    },
    appUser () {
      return this.$store.getters['appUser']
    },
    userGroupInfo () {
      return this.$store.getters['userGroupInfo']
    },
    errorMessage () {
      return this.$store.getters['errorMessage']
    },
    isLoadingResult () {
      return this.$store.getters['isLoadingResult']
    },
    systemMessage () {
      return this.$store.getters['systemMessage']
    }
  },
  created () {
    this.$store.dispatch('checkLogin')
  },
  methods: {
    login () {
      this.$store.dispatch('login')
    },
    logout () {
      this.$store.dispatch('logout')
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/_variables.scss";
.test-mode {
  background: #e2e2e2;
}

.header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  border-bottom: solid 1px lightgrey;

  & > p.heading {
    width: 220px;
  }

  & > p.onload-message-display {
    position: absolute;
    top: 5px;
    left: 52%;
    padding: 2px 10px 2px 10px;
    font-size: 14px;
    font-weight: bold;
    font-family: $font-stack-sans;
    background: #ffe699;
    text-align: center;
  }

  & img {
    width: 22px;
    margin-left: 10px;
    margin-bottom: 5px;
  }

  & > p {
    margin-left: 10px;
    font-size: 24px;
    cursor: pointer;
    font-family: $font-stack-serif;
    margin-bottom: 10px;
  }

  & > .menu {
    display: flex;
    height: 24px;
    margin-left: 70px;
    margin-bottom: 5px;

    @media screen and (max-width: 1200px) {
      display: none;
    }

    & > .menu-item {
      width: 160px;
      text-align: center;
      cursor: pointer;
      font-size: 15px;
      border: solid 1px lightgrey;
      border-bottom: none;
      border-top-left-radius: 5px;
      border-top-right-radius: 5px;
      @include disable-text-select;

      &.router-link-active {
        background-color: lightgrey;
        cursor: context-menu;
      }

      &:not(.router-link-active):hover {
        border-bottom: solid 3px lightgrey;
      }
    }
  }

  & > .control-area {
    display: flex;
    flex-direction: column;
    margin-left: auto;
    margin-bottom: 5px;
    height: 100%;

    @media screen and (max-width: 700px) {
      display: none;
    }

    & > div.login-logout {
      margin-top: auto;

      & > p {
        font-size: 13px;
        text-align: right;
        margin-right: 30px;
        color: $active-text-color;

        & > .icon {
          margin-right: 5px;
          color: grey;
        }

        & > span {
          cursor: pointer;

          &.usergroup-label {
            margin-left: 5px;
          }

          &.usergroup-label:before {
            content: "(";
          }

          &.usergroup-label:after {
            content: ")";
          }

          &:hover {
            text-decoration: underline;
          }
        }

        & > span.separator {
          margin: 0px 7px 0 7px;
          border-left: solid 1px lightgrey;
          color: lightgrey;
        }

      }
    }

    & > p.error-message {
      margin-left:auto;
      padding-right: 10px;
      width: 300px;
      height: 20px;
      margin-bottom: 10px;
      text-align: right;
      color: white;
      font-size: 12px;
      font-weight: bold;
      border-radius: 0 0 0 50px;

      &.active {
        background-color: red;
      }
    }
  }
}
</style>
