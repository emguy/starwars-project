<template>
  <div class="root">
    <div class="manifest-content-head">
      <div class="left-head head">
        <div class="main-head">
          <h2 class="entry-body">
            <span>{{ manifest.product.toUpperCase() }}&nbsp;</span>
            <span>{{ manifest.branch }}&nbsp;</span>
            <span>{{ manifest.buildName }}</span>
            <span
              v-if="manifest.subBuildVersion!==undefined"
            >/{{ manifest.subBuildVersion }}</span>
            <router-link
              class="link"
              :to="{path: manifestUri}"
            >
              <font-awesome-icon
                class="icon"
                icon="external-link-alt"
              />
            </router-link>
          </h2>
          <div class="badges">
            <LabeledBadge
              label="build"
              :message="manifest.lifeCycleStatus"
            />
          </div>
          <div class="verification-list">
            <div
              v-for="(userEntry, index) in compact_verification_list"
              :key="index"
              class="verification-entry"
            >
              <span class="subject">{{ userEntry.subject }}</span>
              <span
                v-if="userEntry.score>0"
                class="score"
              >
                +{{ userEntry.score }}
              </span>
              <span
                v-else
                class="score negative"
              >
                {{ userEntry.score }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="right-head head">
        <div class="main-head">
          <div class="git-head">
            <p class="author">
              <span class="label">Author</span>
              <span>{{ triggeringGit.author }}&nbsp;</span>
              <a
                class="email"
                :href="'mailto:'+triggeringGit.authorEmail"
              >
                {{ triggeringGit.authorEmail }}
              </a>
            </p>
            <p class="subject">
              <span class="label">Subject</span>
              <span>{{ triggeringGit.subject }}</span>
            </p>
          </div>
          <p class="git-message">
            {{ triggeringGit.message }}
          </p>
          <p class="git-tracking-id-list">
            <span class="label">Tracking Id</span>
            <span
              v-for="(item, index) in triggeringGit.trackingIdList"
              :key="index"
              class="tracking-id"
            >
              {{ item }}
            </span>
          </p>
        </div>
      </div>
    </div>
    <div class="manifest-content-head-bottom">
      <div class="left">
        <p>
          <span class="label">Build Started</span>
          <span
            class="value"
          >{{ getFormattedTime(manifest.createdDate) }}</span>
        </p>
        <p>
          <span class="label">Duration</span>
          <span class="value">
            {{ getTimeDiff(manifest.createdDate, lastBuildEndTime) }}
          </span>
        </p>
      </div>
      <div class="right">
        <p>
          <span class="label">Commit Id</span>
          <a
            class="gcr"
            target="_blank"
            :href="triggeringGit.gcr"
          >
            {{ triggeringGit.commitId }}
          </a>
        </p>
        <p>
          <span class="label">Date</span>
          <span class="value">
            {{ getFormattedTime(triggeringGit.committerDate) }}
          </span>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import LabeledBadge from '@/components/widgets/LabeledBadge'

export default {
  components: {
    LabeledBadge
  },
  props: {
    manifest: {
      type: Object,
      default: null
    },
    gitIndex: {
      type: Number,
      default: null
    }
  },
  computed: {
    lastBuildEndTime () {
      let best = this.manifest.createdDate
      for (let job of this.manifest['buildJobs']) {
        if (job['endTime'] && job['endTime'] > best) {
          best = job['endTime']
        }
      }
      return best
    },
    manifestUri () {
      return '/dashboard/manifest/' + this.manifest['id']
    },
    triggeringGit () {
      return this.manifest.git[this.gitIndex]
    },
    buildDate () {
      let rawDate = this.manifest['default']['build date']
      return rawDate
    },
    compact_verification_list () {
      return this.manifest['verificationHistory']
        .filter(entry => entry.score !== 0)
    }
  },
  methods: {
    getBadgeUrl (uri) {
      return process.env.VUE_APP_BACKEND + uri
    },
    getFormattedTime (rawTime) {
      if (!rawTime) {
        return ''
      }
      let datetime = new Date(rawTime)
      let dateItems = datetime.toDateString().split(' ')
      let datestring = `${dateItems[3]}-${dateItems[1]}-${dateItems[2]}`
      let timestring = datetime.toTimeString().split(' ')[0]
      return datestring + ' ' + timestring
    },
    getTimeDiff (start, end) {
      if (!end) {
        return 'N/A'
      }
      let seconds = Math.floor((new Date(end) - new Date(start)) / 1000)
      let minutes = Math.floor(seconds / 60)
      return minutes > 0 ? minutes + ' minutes' : seconds + ' seconds'
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";

span.label {
  display: inline-block;
  font-weight: bold;
  margin-right: 5px;
  &:after {
    content: ":"
  }
}

a.gcr {
  color: blue;
}

a.email {
  color: blue;
  &:before {
    content: "<";
  }
  &:after {
    content: ">";
  }
}

.manifest-content-head-bottom {
  width: 100%;
  display: flex;
  font-size: 13px;
  padding: 0px 4px  4px 10px;
  background-color: lightgrey;
  background-image: linear-gradient(to right, lightgrey, white);
  font-family: $font-stack-serif;

  & > div {
    display: flex;

    &.left {
      flex: 0 0 500px;
    }

    & > p {
      margin-right: 30px;

      & > span.label {
        font-weight: bold;
      }
    }
  }

}

.manifest-content-head {
  display: flex;
  margin-bottom: 10px;
  min-height: 140px;

  & > .head {
    font-family: $font-stack-serif;

    & > .main-head {
      padding-left: 10px;
    }
  }

  & > .left-head {
    flex: 0 0 500px;
    border-right: solid 1px lightgrey;

    & > .main-head {
      & > h2 {
        position: relative;
        margin: 25px 0 10px 0;
        font-size: 24px;
        font-family: $font-stack-serif;
        z-index: -1;

        & > .link {
          display: none;
          position: absolute;
          margin-left: 5px;
          bottom: 10px;

          & > .icon {
            font-size: 13px;
          }
        }

        &:hover > .link {
          display: inline;
        }
      }

      & > .badges {
        display: flex;
        margin-bottom: 10px;
        align-items: center;
      }

      & > .verification-list {
        display: inline-flex;
        flex-wrap: wrap;
        font-size: 12px;
        font-family: $font-stack-serif;

        & > div {
          margin: 0 10px 7px 0;
          background: lightgrey;
          padding: 1px 5px 1px 5px;
          border-radius: 4px;

          & span.subject {
            margin-right: 7px;
          }

          & span.score {
            color: green;
            font-weight: bold;
          }

          & span.negative {
            color: red;
          }
        }
      }
    }
  }
  .right-head {
    font-size: 13px;
    flex-grow: 1;
    overflow: hidden;

    & > .main-head {
      & > .git-head {
        padding-bottom: 6px;
        border-bottom: solid 1px lightgrey;
        margin-bottom: 10px;
      }

      & > p.git-message {
        height: 55px;
        margin-bottom: 7px;
        overflow-y: scroll;
        -ms-overflow-style: none;
        scrollbar-width: none;

        &::-webkit-scrollbar {
          display: none;
        }
      }

      & > p.git-tracking-id-list {
        & > span.tracking-id {
          margin-right: 3px;
        }
      }
    }
  }
}
</style>
