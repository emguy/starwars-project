<template>
  <div>
    <h3>Build Jobs</h3>
    <div class="manifest-jobs-table">
      <div class="table-row table-head">
        <div>Job Name</div>
        <div>Status</div>
        <div>Start Time</div>
        <div>Stop Time</div>
        <div>Duration</div>
        <div>Benchmark</div>
        <div>Log</div>
      </div>
      <div
        v-for="(job, index) in manifest.buildJobs"
        :key="index"
        class="table-row"
      >
        <div>{{ job.name }}</div>
        <div>
          <font-awesome-icon
            v-if="job.status==='failed'"
            class="icon failed"
            icon="times"
          />
          <font-awesome-icon
            v-else-if="job.status==='passing'"
            class="icon passing"
            icon="check"
          />
          <font-awesome-icon
            v-else-if="job.status==='pending'"
            class="icon pending"
            :icon="['far', 'clock']"
          />
          <font-awesome-icon
            v-else-if="job.status==='ongoing'"
            class="icon blinking"
            :icon="['far', 'clock']"
          />
          <font-awesome-icon
            v-else
            class="icon error"
            icon="exclamation"
          />
        </div>
        <div>
          {{ getFormattedTime(job.startTime) }}
        </div>
        <div>
          {{ getFormattedTime(job.endTime) }}
        </div>
        <div>
          {{ getTimeDiff(job.startTime, job.endTime) }}
        </div>
        <div>
          <span v-if="job.benchmark">2000 sec</span>
          <span v-else>N/A</span>
        </div>
        <div>
          <a
            v-if="job.result && job.result.logUrl"
            :href="convertLogUrl(job.result.logUrl)"
            target="_blank"
          >
            <font-awesome-icon
              class="icon"
              icon="desktop"
            />
          </a>
        </div>
      </div>
      <div
        v-if="manifest.buildJobs.length===0"
        class="table-row"
      >
        <div>N/A</div>
        <div>N/A</div>
        <div>N/A</div>
        <div>N/A</div>
        <div>N/A</div>
        <div>N/A</div>
        <div>N/A</div>
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
    }
  },
  methods: {
    convertLogUrl (url) {
      // TODO: This is for backward capability. Will be removed in Feb 2021.
      let oldUrl = 'https://seliius24321.seli.gic.ericsson.se:9998/river/logs'
      let newUrl = 'https://river.internal.ericsson.com/concourse-logs'
      return url.includes(oldUrl) ? url.replace(oldUrl, newUrl) : url
    },
    getFormattedTime (rawTime) {
      if (!rawTime) {
        return '-'
      }
      let datetime = new Date(rawTime)
      let dateItems = datetime.toDateString().split(' ')
      let datestring = `${dateItems[3]}-${dateItems[1]}-${dateItems[2]}`
      let timestring = datetime.toTimeString().split(' ')[0]
      return datestring + ' ' + timestring
    },
    getTimeDiff (start, end) {
      if (!start || !end) {
        return '-'
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
h3 {
  padding-left: 10px;
  font-size: 20px;
  font-family: $font-stack-serif;
  margin: 22px 0px 16px 0px;
  border-bottom: solid 1px lightgrey;
}

.failed {
  color: red;
}

.pending {
  color: yellowgreen;
}

.blinking {
  color: green;
  animation: opacity 0.8s ease-in-out infinite;
  opacity: 1;
}

.passing {
  color: green;
}

.error {
  color: red;
}

div.manifest-jobs-table {
  & div.table-row {
    & > div:nth-child(1) {
      width: 200px;
    }
    & > div:nth-child(2) {
      width: 100px;
      text-align: center;
    }
    & > div:nth-child(3) {
      width: 200px;
    }
    & > div:nth-child(4) {
      width: 200px;
    }
    & > div:nth-child(5) {
      width: 100px;
    }
    & > div:nth-child(6) {
    }
    & > div:nth-child(7) {
      margin-left: auto;
      text-align: center;
      width: 40px;
    }
  }
}

@keyframes opacity {
  0% {
    opacity: 1;
  }

  50% {
    opacity: 0.6
  }

  100% {
    opacity: 0.2;
  }
}

</style>
