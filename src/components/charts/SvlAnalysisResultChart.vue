<template>
  <svg
    class="chart"
    xmlns="http://www.w3.org/2000/svg"
    height="210"
    width="400"
    viewBox="0 0 400 210"
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
          y="10"
          width="16"
          height="10"
          :fill="colors[index]"
          strokeWidth="1"
        />
        <text
          class="legend-text"
          :x="202"
          :y="20"
        >
          {{ labels[index] }}
        </text>
        <text
          class="legend-text"
          :x="330"
          :y="20"
        >
          {{ dataSet[index] }}
        </text>
      </g>
    </g>
    <text
      class="total"
      :x="cx"
      :y="cy"
      :dx="-23"
      :dy="7"
    >{{ dataTotal }}</text>
    <text
      class="title"
      :x="10"
      :y="20"
      :dx="0"
      :dy="0"
    >{{ title }}</text>
  </svg>
</template>
<script>
export default {
  props: {
    result: {
      type: Object,
      default: null
    },
    title: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      chartData: [],
      labels: [
        'matched',
        'weakly-matched',
        'known',
        'version-missing',
        'version-mismatch',
        'filtered',
        'unmatched'
      ],
      colors: ['#690', '#7b3', '#9c0', '#39f', '#c60', '#fc0', '#c00'],
      cx: 80,
      cy: 110,
      radius: 60,
      strokeWidth: 30
    }
  },
  computed: {
    dataSet () {
      return [
        this.result.summary.matched + this.result.summary.ignored,
        this.result.summary.weaklyMatched,
        this.result.summary.known - 12,
        this.result.summary.versionMissing,
        this.result.summary.versionNotMatched,
        12,
        this.result.summary.unmatched
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
