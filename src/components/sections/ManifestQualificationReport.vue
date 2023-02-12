<template>
  <div
    v-if="showSection"
    class="qualification-report"
  >
    <h3>Qualification Report</h3>
    <div class="qualification-summary-list">
      <div
        v-for="(item, index) in resultList"
        :key="index"
        :class="{active: isActiveResult(index)}"
        @click="setActiveResultIndex(index)"
      >
        <QualificationResultChart
          class="donut-chart"
          :title="item.name"
          :qualification-result="item"
        />
      </div>
    </div>
    <div
      class="qualification-table"
    >
      <div class="table-row table-head">
        <div>Failed Tests</div>
        <div>Duration</div>
      </div>
      <div
        v-if="resultList[activeIndex].failed===0"
        class="table-row"
      >
        <div>N/A</div>
        <div>N/A</div>
      </div>
      <div
        v-else
        v-for="(item2, index2) in resultList[activeIndex].failedTests"
        :key="index2"
        class="table-row"
      >
        <div>{{ item2.name }}</div>
        <div>{{ item2.duration }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import QualificationResultChart from
  '@/components/charts/QualificationResultChart'

export default {
  components: {
    QualificationResultChart
  },
  props: {
    manifest: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      activeIndex: 0,
      resultList: []
    }
  },
  computed: {
    showSection () {
      return this.resultList.length > 0
    }
  },
  methods: {
    isActiveResult (index) {
      return this.activeIndex === index
    },
    setActiveResultIndex (index) {
      this.activeIndex = index
    },
    updateResultList () {
      this.resultList = []
      for (let job of this.manifest.buildJobs) {
        if (job.status === 'pending' || job.status === 'error' || !job.result) {
          continue
        }
        if (job.result.type && job.result.type === 'testing-report') {
          this.resultList.push(job.result)
        }
      }
    }
  },
  watch: {
    manifest () {
      this.updateResultList()
    }
  },
  created () {
    this.updateResultList()
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

div.qualification-report {
  & > div.qualification-summary-list {
    display: inline-flex;

    & > div {
      margin-right: 4px;
      height: 198px;
      border: solid 4px white;

      &.active {
        border: solid 4px yellowgreen;
      }

      &:hover {
        cursor: pointer;
      }
    }
  }
}

div.qualification-table {
  & div.table-row {
    & > div:nth-child(1) {
    }
    & > div:nth-child(2) {
      margin-left: auto;
      width: 120px;
    }
    & > div:nth-child(3) {
      width: 70px;
    }
    & > div:nth-child(4) {
      width: 80px;
    }
    & > div:nth-child(5) {
      width: 70px;
    }
  }
}
</style>
