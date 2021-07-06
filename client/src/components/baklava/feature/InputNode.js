import { NodeBuilder } from "@baklavajs/core";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
import store from "@/store/index";

const columns = store.getters["initialData/columns"];

export default new NodeBuilder("InputNode", {
  //   twoColumn: true,
  //   width: 200
})
  .setName("Input")
  .addOutputInterface("OUT")
  .addOption("FeatureOption", "FeatureOption")
  .addOption(
    "Features",
    "ButtonOption",
    () => {
      return { features: columns };
    },
    "FeatureSidebar"
  )
  .addOption("ValueText", "TextOption")
  .onCalculate(n => {
    let result = n.getOptionValue("Features");
    n.getInterface("OUT").value = result;
    n.setOptionValue("ValueText", result);
  })

  .build();
