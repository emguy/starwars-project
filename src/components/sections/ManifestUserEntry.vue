<template>
  <div class="entry">
    <div
      class="entry-heading"
      @click="toggleExpansion"
    >
      <div class="name">
        {{ userEntry.user.displayName }}
      </div>
      <div
        class="score"
        :class="{'negative-score': userEntry.score < 0}"
      >
        {{ formattedRating }}
      </div>
      <div class="title">
        <p>
          {{ userEntry.subject }}
          <span class="subtitle">
            {{ subtitle }}
          </span>
        </p>
      </div>
      <div class="time">
        {{ formattedTime }}
      </div>
    </div>
    <div
      v-if="expanded"
      class="entry-body"
    >
      <div
        class="content"
        v-html="entryBody"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    userEntry: {
      type: Object,
      default: null
    },
    expand: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      expanded: false
    }
  },
  computed: {
    formattedRating () {
      if (this.userEntry.score === 0) {
        return ''
      } else if (this.userEntry.score > 0) {
        return '+' + String(this.userEntry.score)
      }
      return String(this.userEntry.score)
    },
    formattedTime () {
      let datetime = new Date(this.userEntry.timestamp)
      let dateItems = datetime.toDateString().split(' ')
      let datestring = `${dateItems[1]}-${dateItems[2]}`
      let timestring = datetime.toTimeString().split(' ')[0]
      return datestring + ' ' + timestring
    },
    subtitle () {
      if (this.expanded || !this.userEntry.body) {
        return ''
      }
      return this.userEntry.body.substr(0, 100).replace(/(?:\r\n|\r|\n)/g, ' ')
    },
    entryBody () {
      if (!this.expanded || !this.userEntry.body) {
        return ''
      }
      return this.userEntry.body.replace(/\r\n|\r|\n/, '<br/><br/>')
    },
    buildDate () {
      let rawDate = this.manifest['default']['build date']
      return rawDate
    }
  },
  watch: {
    expand (value) {
      this.expanded = value
    }
  },
  methods: {
    toggleExpansion () {
      this.expanded = !this.expanded
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";

.entry {
  font-size: 14px;
  padding:  0 10px 0 10px;
  border: solid lightgrey 1px;
  border-width: 0 1px 1px 1px;
  border-radius: 0 0 6px 6px;

  .entry-heading {
    display: flex;
    cursor: pointer;
    height: 25px;
    min-width: 0;

    & > div.name {
      flex: 0 0 100px;
      overflow: hidden;
      text-overflow: clip;
    }

    & > div.title {
      min-width: 0;
      margin-right: 20px;
      & > p {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;

        & > span.subtitle {
          color: grey;
        }
      }
    }

    & > div.score {
      flex: 0 0 20px;
      font-weight: bold;
      margin-right: 12px;
      text-align: right;
      color: green;

      &.negative-score {
        color: red;
      }
    }

    & > div.time {
      flex: 0 0 120px;
      margin-left: auto;
      margin-right: 10px;
      text-align: right;
    }
  }
  .entry-body {
    display: flex;
    & > div.content {
      text-align: justify;
      margin: 0 20px 0 102px;
      color: grey;
      width: 100%;
    }
  }
}
</style>
