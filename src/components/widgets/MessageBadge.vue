<template>
  <span
    class="message"
    :style="{background: color}"
  ><slot /></span>
</template>

<script>
export default {
  name: 'MessageBadge',
  props: {
    type: {
      type: String,
      default: 'passed'
    }
  },
  data () {
    return {
      colorMap: {
        'passed': '#33cc33',
        'failed': '#ff6600'
      }
    }
  },
  computed: {
    color () {
      return this.colorMap[this.type]
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/_variables.scss";
span.message {
  font-size: 12px;
  font-family: $font-stack-sans;
  text-shadow: 1px 1px 8px #333333;
  color: white;
  @include disable-text-select;
  cursor: default;
  font-weight: normal;
  background: #666666;
  padding: 0px 5px;
  border-radius: 3px;
  margin-right: 5px;
}
</style>
