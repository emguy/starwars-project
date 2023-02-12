<template>
  <svg
    class="chart"
    xmlns="http://www.w3.org/2000/svg"
    height="190"
    width="300"
    viewBox="0 0 300 190"
  >
    <rect
      width="100%"
      height="100%"
      fill="#ecf9f2"
    />
    <g>
      <g
        v-for="(value, index) in dataSet"
        :key="index"
      >
        <circle
          :cx="cx"
          :cy="cy"
          :r="radius"
          fill="transparent"
          :stroke="colors[index]"
          :stroke-width="strokeWidth"
          :transform="returnCircleTransformValue(index)"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="calculateStrokeDashOffset(value, circumference)"
        />
      </g>
    </g>
    <g>
      <g
        v-for="(value, index) in dataSet"
        :key="index"
        :transform="returnLegendTransformValue(index)"
      >
        <rect
          x="180"
          y="50"
          width="16"
          height="10"
          :fill="colors[index]"
          strokeWidth="1"
        />
        <text
          class="legend-text"
          :x="202"
          :y="60"
        >
          {{ labels[index] }}
        </text>
        <text
          class="legend-text"
          :x="255"
          :y="60"
        >
          {{ dataSet[index] }}
        </text>
      </g>
    </g>
    <text
      class="total"
      :x="cx"
      :y="cy"
      :dx="-26"
      :dy="7"
    >{{ dataTotal }}</text>
    <text
      class="title"
      :x="10"
      :y="16"
      :dx="0"
      :dy="0"
    >{{ title }}</text>
  </svg>
</template>
<script>
export default {
  name: 'QualificationResultChart',
  props: {
    qualificationResult: {
      type: Object,
      default: null
    },
    title: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      chartData: [],
      labels: ['passed', 'failed', 'errors', 'filtered', 'skipped'],
      colors: ['#9c0', '#f30', '#600', '#39f', '#ccc'],
      cx: 80,
      cy: 110,
      radius: 60,
      strokeWidth: 30
    }
  },
  computed: {
    dataSet () {
      return [
        this.qualificationResult.passed,
        this.qualificationResult.failed,
        this.qualificationResult.errors,
        this.qualificationResult.filtered,
        this.qualificationResult.skipped
      ]
    },
    circumference () {
      return 2 * Math.PI * this.radius
    },
    degrees () {
      let degrees = []
      let angleOffset = -90
      for (let i = 0; i < this.dataSet.length; ++i) {
        degrees.push(angleOffset)
        angleOffset = this.dataPercentage(this.dataSet[i]) * 360 + angleOffset
      }
      return degrees
    },
    dataTotal () {
      return this.dataSet.reduce((acc, val) => acc + val)
    }
  },
  methods: {
    calculateStrokeDashOffset (dataVal, circumference) {
      const strokeDiff = this.dataPercentage(dataVal) * circumference
      return circumference - strokeDiff
    },
    dataPercentage (dataVal) {
      return dataVal / this.dataTotal
    },
    returnCircleTransformValue (index) {
      return `rotate(${this.degrees[index]}, ${this.cx}, ${this.cy})`
    },
    returnLegendTransformValue (index) {
      return 'translate(0, yOffset)'.replace('yOffset', 25 * index)
    }
  }
}
</script>
<style scoped lang="scss">
@import "@/styles/_variables.scss";
text {
  pointer-events: none;
}
text.legend-text {
  font-size: 12px;
}
text.total {
  font-size: 22px;
}
text.title {
  font-size: 14px;
}
</style>
