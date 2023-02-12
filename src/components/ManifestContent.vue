<template>
  <div
    class="root"
    v-if="manifest"
    id="manifest-content"
  >
    <ManifestControlArea
      class="manifest-control-area"
      :manifest="manifest"
    />
    <ManifestContentHead
      :manifest="manifest"
      :git-index="gitIndex"
    />
    <ManifestGit
      :manifest="manifest"
      :git-index="gitIndex"
      @gitUpdated="updateGitIndex"
    />
    <ManifestJobList :manifest="manifest" />
    <ManifestMegatar :manifest="manifest" />
    <ManifestUrlList :manifest="manifest" />
    <ManifestQualificationReport :manifest="manifest" />
    <ManifestUserHistory :manifest="manifest" />
    <ManifestSvlAnalysisReport :manifest="manifest" />
  </div>
</template>

<script>
import ManifestContentHead from '@/components/ManifestContentHead'
import ManifestControlArea from '@/components/ManifestControlArea'
import ManifestGit from '@/components/sections/ManifestGit'
import ManifestUserHistory from '@/components/sections/ManifestUserHistory'
import ManifestJobList from '@/components/sections/ManifestJobList'
import ManifestUrlList from '@/components/sections/ManifestUrlList'
import ManifestQualificationReport from
  '@/components/sections/ManifestQualificationReport'
import ManifestSvlAnalysisReport from
  '@/components/sections/ManifestSvlAnalysisReport'
import ManifestMegatar from '@/components/sections/ManifestMegatar'

export default {
  components: {
    ManifestContentHead,
    ManifestControlArea,
    ManifestQualificationReport,
    ManifestSvlAnalysisReport,
    ManifestUserHistory,
    ManifestJobList,
    ManifestUrlList,
    ManifestMegatar,
    ManifestGit
  },
  props: {
    'manifest': {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      'gitIndex': 0
    }
  },
  methods: {
    updateGitIndex (index) {
      console.log(index)
      this.gitIndex = index
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";
.manifest-control-area {
  position: absolute;
  top: 35px;
  left: 0px;
}

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
