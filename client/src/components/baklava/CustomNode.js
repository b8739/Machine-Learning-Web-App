import { NodeBuilder } from "@baklavajs/core";
import MyOption from "@/components/baklava/MyOption.vue";
import ParameterSidebar from "@/components/baklava/algorithm/ParameterSidebar.vue";

export default new NodeBuilder("CustomNodeWithBuilder", {
  twoColumn: true,
  width: 200
})
  .setName("Custom")
  .addInputInterface("Input")
  .addOutputInterface("Output")
  // .addOption("MyOption", "MyOption", () => {
  //   return { parameters: ["a", "b", "c"] };
  // })
  .addOption(
    "Parameter",
    "ButtonOption",
    () => {
      return {
        parameters: [
          "n_estimators",
          "learning_rate",
          "gamma",
          "eta",
          "subsample",
          "colsample_bytree",
          "max_depth"
        ]
      };
    },
    "ParameterSidebar"
  )

  .addOption("ValueText", "TextOption")
  .onCalculate(n => {
    let result = n.getOptionValue("Parameter");

    n.getInterface("Output").value = result;
    n.setOptionValue("ValueText", result);
  })
  .build();
