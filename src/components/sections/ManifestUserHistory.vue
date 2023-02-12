<template>
  <div class="review-history">
    <h3>Delivery Flow</h3>
    <div class="review-history-bar">
      <ManifestContentUserInput
        class="outside-content"
        :show="showUserInputDialog"
        @hideUserInput="toggleShowUserInputDialog"
      />
      <div class="inner-content">
        <div
          v-if="isLoggedIn"
          class="btn"
        >
          <button
            class="reply-btn"
            @click="toggleShowUserInputDialog"
          >
            Add New Post ...
          </button>
        </div>
        <div
          class="expand-collapse"
          @click="toggleExpandAllUserEntry"
        >
          <span v-if="expandAllUserEntry">- Collapse All</span>
          <span v-else>+ Expand All</span>
        </div>
      </div>
    </div>
    <ul>
      <ManifestContentUserEntry
        v-for="(entry, index) in manifest.verificationHistory"
        :key="index"
        :expand="expandAllUserEntry"
        :user-entry="entry"
      />
    </ul>
  </div>
</template>

<script>
import ManifestContentUserEntry from '@/components/sections/ManifestUserEntry'
import ManifestContentUserInput from '@/components/sections/ManifestUserInput'

export default {
  components: {
    ManifestContentUserEntry,
    ManifestContentUserInput
  },
  props: {
    'manifest': {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      expandAllUserEntry: false,
      showUserInputDialog: false
    }
  },
  computed: {
    isLoggedIn () {
      return this.$store.getters['isLoggedIn']
    }
  },
  watch: {
    manifest () {
      this.showUserInputDialog = false
    }
  },
  methods: {
    toggleExpandAllUserEntry () {
      this.expandAllUserEntry = !this.expandAllUserEntry
    },
    toggleShowUserInputDialog () {
      this.showUserInputDialog = !this.showUserInputDialog
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";
h3 {
  padding-left: 10px;
  font-size: 20px;
  font-family: $font-stack-serif;
  margin: 22px 0px 16px 0px;
  border-bottom: solid 1px lightgrey;
}

div.review-history {
  & > div.review-history-bar {
    position: relative;
    background: lightgrey;
    border-radius: 3px 3px 0 0;
    @include disable-text-select;

    & div.outside-content {
      z-index: 2;
      position: absolute;
      bottom: 33px;
    }

    & > div.inner-content {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 28px;

      & > div.btn {
        margin-left: 10px;

        & > button {
          padding: 0 5px 0 5px;
          font-size: 12px;
        }
      }

      & div.expand-collapse {
        margin-left: auto;
        margin-right: 40px;
        font-size: 12px;
        cursor: pointer;
        color: blue;
      }
    }
  }
}
</style>
