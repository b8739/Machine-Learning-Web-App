export function getCount(datasetLength) {
  return Math.round(datasetLength * 0.05);
  // data111.csv같은 경우 0.05
}
export function getRandom(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

export function getRandomArray(min, max) {
  let count = this.getCount(max);
  if (max - min + 1 < count) return;
  // 배열 생성
  let randomArray = [];
  while (1) {
    let index = this.getRandom(min, max);
    // 중복 여부 체크
    if (randomArray.indexOf(index) > -1) {
      continue;
    }
    randomArray.push(index);
    // 원하는 배열 갯수 만족 시 종료
    if (randomArray.length == count) {
      break;
    }
  }
  // 정렬
  let sortedRandomArray = randomArray.sort(function(a, b) {
    return a - b;
  });
  return sortedRandomArray;
}
//preprocess methods
export function randomizeDataset(dataset_unrandomized, dataset_randomized, randomIndexArray) {
  for (let i = 0; i < randomIndexArray.length; i++) {
    dataset_randomized.push(dataset_unrandomized[randomIndexArray[i]]); //이게 정말 randomize되는것
    // targetArray.push(dataset_unrandomized[i]);
  }
  return dataset_randomized;
}
export function randomizeDate(dataset_unrandomized, dataset_randomized, randomIndexArray) {
  for (let i = 0; i < randomIndexArray.length; i++) {
    dataset_randomized.push(dataset_unrandomized[randomIndexArray[i]]); //이게 정말 randomize되는것
    // targetArray.push(dataset_unrandomized[i]);
  }
}
