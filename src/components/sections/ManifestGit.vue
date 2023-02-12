<template>
  <div>
    <h3>Git</h3>
    <div class="git-table">
      <div class="table-row table-head">
        <div>Repository</div>
        <div>Commit</div>
        <div>Date</div>
        <div>Subject</div>
      </div>
      <div
        v-for="(item, index) in manifest.git"
        :key="index"
        class="table-row"
      >
        <div>{{ item.project }}</div>
        <div>
          <a
            class="gcr"
            target="_blank"
            :href="item.gcr"
          >
            {{ getShortCommitId(item.commitId) }}
          </a>
        </div>
        <div>{{ getFormattedTime(item.authorDate) }}</div>
        <div
          :class="{active:isActiveIndex(index)}"
          @click="$emit('gitUpdated', index)"
        >
          <span v-if="isActiveIndex(index)">
            <font-awesome-icon
              class="icon"
              icon="leaf"
              style="color:green"
            />
          </span>
          {{ item.subject }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    manifest: {
      type: Object,
      default: null
    },
    gitIndex: {
      type: Number,
      default: 0
    }
  },
  methods: {
    isActiveIndex (index) {
      return index === this.gitIndex
    },
    getFormattedTime (rawTime) {
      if (!rawTime) {
        return 'N/A'
      }
      let datetime = new Date(rawTime)
      let dateItems = datetime.toDateString().split(' ')
      let datestring = `${dateItems[3]}-${dateItems[1]}-${dateItems[2]}`
      let timestring = datetime.toTimeString().split(' ')[0]
      return datestring + ' ' + timestring
    },
    getShortCommitId (longId) {
      return longId.substr(0, 8)
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

a.gcr {
  color: blue;
  font-family: $font-stack-mono;
}

div.git-table {
  & div.table-row {
    & > div:nth-child(1) {
      width: 300px;
    }
    & > div:nth-child(2) {
      width: 200px;
    }
    & > div:nth-child(3) {
      width: 360px;
    }
    & > div:nth-child(4) {
      width: 100%;
      cursor: pointer;
    }
  }
}
</style>
