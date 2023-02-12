<template>
  <div class="badge">
    <div class="label">
      {{ label }}
    </div>
    <div
      class="message"
      :class="{ shine: isOngoing }"
      :style="{background: color}"
    >
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'LabeledBadge',
  props: {
    label: {
      type: String,
      default: 'passing'
    },
    message: {
      type: String,
      default: '0'
    }
  },
  data () {
    return {
      colorMap: {
        'build': {
          'passing': '#33cc33',
          'ongoing': '#6FBC8F',
          'error': '#ff0000',
          'failed': '#ff6600',
          'inactive': '#999999',
          'initiated': '#999999',
          'expired': '#ff0000'
        }
      }
    }
  },
  computed: {
    isOngoing () {
      return this.message === 'ongoing'
    },
    color () {
      return this.colorMap[this.label][this.message]
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/_variables.scss";
div.badge {
  font-size: 12px;
  font-family: $font-stack-sans;
  text-shadow: 1px 1px 8px #333333;
  color: white;
  @include disable-text-select;
  cursor: default;
  font-weight: normal;
  z-index: -1;
  & > div {
    display: inline-block;
  }
  & > div.label {
    background: #666666;
    padding: 1px 5px;
    border-radius: 4px 0 0 4px;
  }
  & > div.message {
    position: relative;
    background: #33cc33;
    padding: 1px 5px;
    border-radius: 0 4px 4px 0;
  }

  div.shine:after {
    content:'';
    top:0;
    transform:translateX(100%);
    width:20px;
    height:100%;
    position: absolute;
    z-index:1;
    animation: slide 2s infinite;
    background: -moz-linear-gradient(left,
      rgba(255,255,255,0) 0%,
      rgba(255,255,255,0.8) 50%,
      rgba(128,186,232,0) 99%,
      rgba(125,185,232,0) 100%); /* FF3.6+ */
    background: -webkit-linear-gradient(left,
      rgba(255,255,255,0) 0%,
      rgba(255,255,255,0.8) 50%,
      rgba(128,186,232,0) 99%,
      rgba(125,185,232,0) 100%); /* Chrome10+,Safari5.1+ */
  }
}

@keyframes slide {
  0% {transform:translateX(-450%);}
  100% {transform:translateX(-80%);}
}
</style>
