import { NodeBuilder } from "@baklavajs/core";

export default new NodeBuilder("DisplayNode", {
  twoColumn: true,
  width: 200
})
  .setName("Display")
  .addInputInterface("Input")
  .addOption("ValueText", "InputOption")

  .onCalculate(n => {
    let result = n.getInterface("Input").value;

    n.setOptionValue("ValueText", result);
  })
  .build();
