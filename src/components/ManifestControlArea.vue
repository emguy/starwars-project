<template>
  <div
    v-if="$router.currentRoute.name.startsWith('ManifestBrowser')"
  >
    <div class="btn-group">
      <div
        class="btn"
        @click="scrollToTop"
      >
        <font-awesome-icon
          class="icon"
          icon="chevron-up"
        />
        <p>Top</p>
      </div>
      <div
        class="btn"
        @click="copyToClipBoard(manifestUrl)"
      >
        <font-awesome-icon
          class="icon"
          icon="link"
        />
        <p>Copy Url</p>
      </div>
      <div
        class="btn"
        @click="toggleShowDeletionDialog"
      >
        <font-awesome-icon
          class="icon"
          :icon="['far', 'trash-alt']"
        />
        <p>Delete</p>
      </div>
      <div class="btn">
        <a
          class="link"
          :href="manifestJsonUrl"
          target="_blank"
        >
          <font-awesome-icon
            class="icon"
            icon="glasses"
          />
        </a>
        <p>json</p>
      </div>
      <div class="btn">
        <font-awesome-icon
          class="icon"
          icon="sync"
          @click="reloadManifest"
        />
        <p>Refresh</p>
      </div>
      <div class="btn">
        <router-link
          class="link"
          :to="{path: manifestUri}"
        >
          <font-awesome-icon
            class="icon"
            icon="external-link-alt"
          />
        </router-link>
        <p>New Tab</p>
      </div>
    </div>
    <div
      v-if="showDeletionDialog"
      class="delete-confirmation"
    >
      <p>
        <span v-if="isDeletionAllowed">
          Click delete to remove the current manifest.
          <br>
          <span class="manifest-name"> {{ manifestName }} </span>
        </span>
        <span v-else>
          Please login with admin privilege for this operation.
        </span>
      </p>
      <div class="buttons">
        <button
          class="btn-cancel"
          v-if="!isDeletionAllowed"
          @click="toggleShowDeletionDialog"
        >
          Okay
        </button>
        <button
          class="btn-delete"
          v-if="isDeletionAllowed"
          @click="removeCurrentManifest"
        >
          Delete
        </button>
        <button
          class="btn-cancel"
          v-if="isDeletionAllowed"
          @click="toggleShowDeletionDialog"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    'manifest': {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      showDeletionDialog: false
    }
  },
  computed: {
    isTestMode () {
      return this.$route.name.endsWith(':test')
    },
    isDeletionAllowed () {
      return this.isLoggedIn && this.userGroupInfo.groupName === 'admin'
    },
    isLoggedIn () {
      return this.$store.getters['isLoggedIn']
    },
    userGroupInfo () {
      return this.$store.getters['userGroupInfo']
    },
    manifestId () {
      return this.manifest['id']
    },
    manifestName () {
      return this.manifest['product'] + ' ' + this.manifest['branch'] +
        ' ' + this.manifest['buildName']
    },
    manifestUri () {
      let manifestUri = this.isTestMode ? '/manifest-test/' : '/manifest/'
      return manifestUri + this.manifest['id']
    },
    manifestUrl () {
      return window.location.origin +
        this.$router.options.base + this.manifestUri
    },
    manifestJsonUrl () {
      let queryUrl = this.isTestMode ? '?database=testdb' : ''
      return process.env.VUE_APP_BACKEND + '/dashboard/api/v1/manifest/' +
        this.manifest['id'] + queryUrl
    }
  },
  methods: {
    removeCurrentManifest () {
      this.showDeletionDialog = false
      this.$store.dispatch(
        'manifestBrowser/removeCurrentManifest',
        { 'isTestMode': this.isTestMode })
    },
    reloadManifest () {
      this.$store.dispatch(
        'manifestBrowser/reloadCurrentManifest',
        { 'isTestMode': this.isTestMode })
    },
    copyToClipBoard (text) {
      navigator.clipboard.writeText(text).then(() => {
        this.$store.dispatch('setSystemMessage', 'copied to the clipboard')
      })
    },
    toggleShowDeletionDialog () {
      this.showDeletionDialog = !this.showDeletionDialog
    },
    scrollToTop () {
      let targetDiv = document.getElementById('manifest-content')
      targetDiv.scrollTop = 0
    }
  },
  watch: {
    manifestId () {
      this.showDeletionDialog = false
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";
div.btn-group {
  display: flex;
  z-index: -2;

  & > div.btn {
    position: relative;
    text-align: center;
    background-color: #ccc;
    width: 40px;
    height: 18px;
    font-size: 12px;

    & > .link, & > a {
      display: block;
      text-align: center;
      width: 100%;
      height: 100%;
    }

    &:hover {
      cursor: pointer;
      background-color: #776;
    }

    & .icon {
      color: white;
    }

    & > p {
      position: absolute;
      top: -14px;
      display: none;
      background: #776;
      font-size: 9px;
      color: white;
      text-align: center;
      width: 100%;
      max-width: 120px;
    }

    &:hover p {
      display: block;
    }

  }
}

.delete-confirmation {
  background-color: lightgrey;
  margin-top: 1px;
  width: 270px;
  z-index: 30;
  font-size: 12px;
  padding: 5px;

  & > p {
    margin-bottom: 7px;
  }

  & .manifest-name {
    font-weight: bold;
    color: #e30;
  }

  & > .buttons {
    display: flex;

    & > button {
      width: 60px;
      text-align: center;
      height: 18px;
      font-size: 13px;
      box-shadow: none;
      margin-right: 10px;
      border-width: 1px;

      &.btn-delete {
        background-color: lightblue;
      }
      &.btn-cancel {
        margin-left: auto;
      }
    }
  }
}
</style>
