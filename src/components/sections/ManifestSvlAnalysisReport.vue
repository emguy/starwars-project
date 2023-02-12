<template>
  <div
    v-if="result && result.summary"
    class="svl-analysis-report"
  >
    <h3>SVL Analysis Report</h3>
    <div class="qualification-summary-list">
      <SvlAnalysisResultChart
        class="donut-chart"
        title="SVL Analysis Result"
        :result="result"
      />
    </div>
    <div class="svl-table unmatched">
      <div class="table-row table-head">
        <div>Unidentified Artifacts</div>
      </div>
      <div
        v-for="(item, index) in
          result.unmatched"
        :key="index"
        class="table-row"
      >
        <div>
          {{ item.path }}<span
            v-if="item.version"
            class="version"
          >{{ item.version }}</span>
        </div>
      </div>
      <div
        class="table-row"
        v-if="result.unmatched.length===0"
      >
        <div>N/A</div>
      </div>
    </div>
    <div class="svl-table version-not-matched">
      <div class="table-row table-head">
        <div>Version-Not-Matched Artifacts</div>
        <div>Dictionary Mapping</div>
        <div>Matched SVL Entry</div>
      </div>
      <div
        v-for="(item, index) in
          result.versionNotMatched"
        :key="index"
        class="table-row"
      >
        <div>
          {{ item.path }}<span
            v-if="item.version"
            class="version"
          >{{ item.version }}</span>
        </div>
        <div>{{ item.mapped_name }}</div>
        <div>
          {{ item.matched_svl.name }}<span
            v-if="item.matched_svl.version"
            class="version"
          >{{ item.matched_svl.version }}</span>
        </div>
      </div>
      <div
        v-if="result.versionNotMatched.length===0"
        class="table-row"
      >
        <div>N/A</div>
        <div>N/A</div>
        <div>N/A</div>
      </div>
    </div>
    <div class="svl-table version-missing">
      <div class="table-row table-head">
        <div>Artifacts Without Version</div>
        <div>Dictionary Mapping</div>
        <div>Matched SVL Entry</div>
      </div>
      <div
        v-for="(item, index) in
          result.versionMissing"
        :key="index"
        class="table-row"
      >
        <div>{{ item.path }}</div>
        <div>{{ item.mapped_name }}</div>
        <div>
          {{ item.matched_svl.name }}<span
            v-if="item.matched_svl.version"
            class="version"
          >{{ item.matched_svl.version }}</span>
        </div>
      </div>
      <div
        v-if="result.versionMissing.length===0"
        class="table-row"
      >
        <div>N/A</div>
        <div>N/A</div>
        <div>N/A</div>
      </div>
    </div>
  </div>
</template>

<script>
import SvlAnalysisResultChart from
  '@/components/charts/SvlAnalysisResultChart'

export default {
  components: {
    SvlAnalysisResultChart
  },
  props: {
    manifest: {
      type: Object,
      default: null
    }
  },
  computed: {
    result () {
      for (let job of this.manifest.buildJobs) {
        if (job.name === 'svl-analysis') {
          return job.result
        }
      }
      return null
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

span.version {
  margin-left: 5px;
  padding: 1px 5px;
  font-size: 12px;
  background-color: #690;
  color: #fff;
  border-radius: 3px;
  cursor: default;
}

div.version-not-matched, div.version-missing {
  & div.table-row {
    & > div:nth-child(1) {
      width: 400px;
    }
    & > div:nth-child(2) {
      width: 300px;
    }
    & > div:nth-child(3) {
    }
  }
}
</style>
