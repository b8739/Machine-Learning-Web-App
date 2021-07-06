import { NodeBuilder } from "@baklavajs/core";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
import store from "@/store/index";

const columns = store.getters["initialData/columns"];

export default new NodeBuilder("TargetNode", {})
  .setName("Target")
  .addInputInterface("IN")
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
    let result = n.getInterface("IN").value;
    console.log(result);
    n.setOptionValue("ValueText", result);
  })
  .build();
