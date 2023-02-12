<template>
  <ul @scroll="loadMoreManifests">
    <div class="manifest-list-head">
      <span> {{ currentProduct.toUpperCase() }} </span>
    </div>
    <li
      v-for="(item, index) in queryResult"
      :key="index"
      :class="{active:isActive(index)}"
      @click="setActiveIndex(index)"
    >
      <div class="entry-index">
        {{ index + 1 }}
      </div>
      <div class="entry-body">
        <p>
          <span>{{ getShortStr(item.branch) }}&nbsp;</span>
          <span>{{ item.buildName }}</span>
          <span
            v-if="item.subBuildVersion!==undefined"
          >/{{ item.subBuildVersion }}
          </span>
        </p>
        <div class="badges">
          <LabeledBadge
            label="build"
            :message="item.lifeCycleStatus"
          />
        </div>
      </div>
      <div class="entry-status">
        <div
          v-if="item.verificationStatus < 0"
          class="yellow"
        />
        <div
          v-if="item.verificationStatus > 0"
          class="green"
        />
      </div>
    </li>
    <li v-if="isLoadingResult">
      <ThreeDotsLoadingEffect />
    </li>
  </ul>
</template>

<script>
import LabeledBadge from '@/components/widgets/LabeledBadge'
import ThreeDotsLoadingEffect from '@/components/widgets/ThreeDotsLoadingEffect'

export default {
  components: {
    LabeledBadge,
    ThreeDotsLoadingEffect
  },
  computed: {
    activeResultIndex () {
      return this.$store.getters['manifestBrowser/activeResultIndex']
    },
    queryResult () {
      return this.$store.getters['manifestBrowser/queryResult']
    },
    currentProduct () {
      return this.$store.getters['manifestBrowser/currentProduct']
    },
    isLoadingResult () {
      return this.$store.getters['isLoadingResult']
    }
  },
  methods: {
    loadMoreManifests () {
      let leftPane = document.getElementsByClassName('left-pane')[0]
      let bottomOfWindow =
        leftPane.scrollHeight - leftPane.scrollTop < leftPane.clientHeight + 5
      if (!this.isLoadingResult && bottomOfWindow) {
        this.$store.dispatch('manifestBrowser/loadMoreResult')
      }
    },
    isActive (index) {
      return index === this.activeResultIndex
    },
    setActiveIndex (index) {
      this.$store.dispatch('manifestBrowser/setActiveResultIndex', index)
    },
    getShortStr (str) {
      return str.length < 15 ? str : str.substr(8)
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/_variables.scss";

ul {
  position:relative;
}

div.manifest-list-head {
  z-index: 1;
  position:fixed;
  padding-left: 20px;
  height: 25px;
  width: 304px;
  background-image: linear-gradient(to right, lightgrey, white);
}

li {
  display: flex;
  align-items: center;
  height: 60px;
  border-bottom: dotted 1px grey;

  &:nth-child(2) {
    margin-top: 25px;
  }

  &.active {
    background-color: $secondary-bg-color-active;
    color: white;
  }

  & > .entry-index {
    width: 45px;
    text-align: center;
  }

  & > .entry-body > p {
    margin: 3px 0;

    & > div.badges {
      display: flex;
      align-items: center;
    }
  }

  & > .entry-status {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    margin-left: auto;
    height: 100%;

    & > div {
      height: 15px;
      width: 10px;
    }

    & > div.green {
      background: yellowgreen;
    }

    & > div.yellow {
      background: #f0de54;
    }
  }
}
</style>
