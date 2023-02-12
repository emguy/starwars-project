<template>
  <div
    class="urls"
    v-if="binaryUrl || reldocUrl"
  >
    <h3>Downloads</h3>
    <ul>
      <li v-if="reldocUrl">
        <a :href="reldocUrl">
          <font-awesome-icon
            class="icon"
            icon="file-pdf"
          />
          <p>release notes</p>
        </a>
      </li>
      <li v-if="binaryUrl">
        <a :href="binaryUrl">
          <font-awesome-icon
            class="icon"
            icon="download"
          />
          <p>rpm</p>
        </a>
      </li>
      <li v-if="megatarUrl">
        <a
          :href="megatarUrl"
          target="_blank"
        >
          <font-awesome-icon
            class="icon"
            icon="download"
          />
          <p>mega-tar</p>
        </a>
      </li>
    </ul>
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
    binaryUrl () {
      return this.manifest.urls.binaryUrl
    },
    reldocUrl () {
      return this.manifest.urls.reldocUrl
    },
    megatarUrl () {
      return this.manifest.urls.megatarUrl
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

.urls > ul {
  display: flex;
  flex-wrap: wrap;

  & > li {
    margin: 0 10px;
    height: 100px;
    width: 100px;

    & > a {
      display: block;
      height: 100%;
      width: 100%;
      background-color: $primary-bg-color;
      text-align: center;

      &:hover {
      background-color: $primary-bg-color-active;
      }

      & > .icon {
        font-size: 24px;
        margin-top: 33px;
        margin-bottom: 19px;
      }

      & > p {
        font-size: 10px;
        text-align: center;
      }
    }
  }
}
</style>
