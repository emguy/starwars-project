<template>
  <div v-if="showContent">
    <h3>Megatar Content</h3>
    <div class="megatar">
      <div v-if="internalImages.length > 0">
        <div class="image-list-table">
          <div class="table-row table-head">
            <div>Internal Images</div>
            <div>Image Version</div>
            <div>Full Image Name</div>
            <div />
          </div>
          <div
            v-for="(item, index) in internalImages"
            :key="index"
            class="table-row"
          >
            <div>{{ getBaseImageName(item.name) }}</div>
            <div>
              <span class="version">{{ item.version }}</span>
            </div>
            <div>
              <span class="irepo">{{ getImageRepoPrefix(item.name) }}</span>
              <span>/</span>
              <span class="iname">{{ getBaseImageName(item.name) }}</span>
              <span>:</span>
              <span class="itag">{{ item.tag }}</span>
            </div>
            <div>
              <font-awesome-icon
                class="icon"
                :icon="['far', 'copy']"
                @click="copyToClipBoard(item.name + ':' + item.tag)"
              />
            </div>
          </div>
        </div>
      </div>
      <div v-if="internalCharts.length > 0">
        <div class="chart-list-table">
          <div class="table-row table-head">
            <div>Internal Helm Charts</div>
            <div>Chart Version</div>
            <div>ARM Repo Location</div>
            <div>Download</div>
          </div>
          <div
            v-for="(item, index) in internalCharts"
            :key="index"
            class="table-row"
          >
            <div>{{ item.sourceFolder }}</div>
            <div>
              <span class="version">{{ item.version }}</span>
            </div>
            <div>
              <a
                class="repo-url"
                v-if="item.repository"
                :href="item.repository + '/' + item.name"
                target="_blank"
              >
                {{ getRepoProjectName(item.repository) + '/' + item.name }}
              </a>
            </div>
            <div>
              <a
                class="link"
                v-if="item.repository"
                target="_blank"
                :href="getChartUrl(item)"
              >
                <font-awesome-icon
                  class="icon"
                  icon="download"
                />
              </a>
            </div>
          </div>
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
    }
  },
  computed: {
    showContent () {
      return this.result && this.result['version'] !== undefined
    },
    result () {
      for (let job of this.manifest.buildJobs) {
        if (job.name === 'generate-megatar') {
          return job['result']
        }
      }
      return null
    },
    internalImages () {
      let images = []
      if (!this.result || !this.result['internalDependencies']) {
        return images
      }
      for (let entry of this.result['internalDependencies']) {
        if (entry['images']) {
          images.push(...entry['images'])
        }
      }
      return images
    },
    internalCharts () {
      let charts = []
      if (!this.result || !this.result['internalDependencies']) {
        return charts
      }
      for (let entry of this.result['internalDependencies']) {
        if (entry['charts']) {
          charts.push(...entry['charts'])
        }
      }
      return charts
    }
  },
  methods: {
    copyToClipBoard (text) {
      navigator.clipboard.writeText(text).then(() => {
        this.$store.dispatch('setSystemMessage', 'copied to the clipboard')
      })
    },
    getChartUrl (item) {
      let chartFileName = item['name'] + '-' + item['version'] + '.tgz'
      return [item['repository'], item['name'], chartFileName].join('/')
    },
    getBaseImageName (fullImageName) {
      return fullImageName.split('/').slice(-1)[0]
    },
    getImageRepoPrefix (fullImageName) {
      let newLength = fullImageName.length -
        this.getBaseImageName(fullImageName).length - 1
      return fullImageName.substr(0, newLength)
    },
    getRepoProjectName (repoUrl) {
      return repoUrl.split('/').slice(-1)[0]
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
div.image-list-table {
  & div.table-row {
    & > div:nth-child(1) {
      width: 320px;
    }
    & > div:nth-child(2) {
      width: 120px;
      cursor: pointer;
    }
    & > div:nth-child(3) {
      width: 600px;
    }
    & > div:nth-child(4) {
      margin-left: auto;
      text-align: right;
      cursor: pointer;
      color: grey;
    }
  }
}
div.chart-list-table {
  & div.table-row {
    & > div:nth-child(1) {
      width: 320px;
    }
    & > div:nth-child(2) {
      width: 120px;
      cursor: pointer;
    }
    & > div:nth-child(3) {
      cursor: pointer;
    }
    & > div:nth-child(4) {
      margin-left: auto;
      width: 80px;
      text-align: right;
      cursor: pointer;
    }
  }
}
span.irepo {
  color: grey;
}
span.iname {
  color: grey;
}
span.itag {
  color: grey;
  font-weight: bold;
}
span.version {
  margin-left: 5px;
  padding: 1px 5px;
  font-size: 12px;
  background-color: #690;
  color: #fff;
  border-radius: 3px;
  cursor: default;
}
a.repo-url {
  color: blue;
  font-family: $font-stack-mono;
}
</style>
