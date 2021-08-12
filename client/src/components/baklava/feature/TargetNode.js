import { NodeBuilder } from "@baklavajs/core";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
import store from "@/store/modules/fundamental/initialData";

const columns = store.state.columns;

export default new NodeBuilder("TargetNode", {})
  .setName("Target")
  .addInputInterface("In")
  .addOutputInterface("Out")
  // .addOption("FeatureOption", "FeatureOption")
  .addOption(
    "Features",
    "ButtonOption",
    () => {
      return { features: columns };
    },
    "FeatureSidebar"
  )

  // .addOption("ValueText", "TextOption")
  .onCalculate(n => {
    let nodeResult = n.getInterface("In").value;
    let targets = n.getOptionValue("Features");
    if (nodeResult != null) {
      nodeResult["targets"] = targets;
      n.getInterface("Out").value = nodeResult;
      return nodeResult;
    }

    // n.setOptionValue("ValueText", result);
  })
  .build();
