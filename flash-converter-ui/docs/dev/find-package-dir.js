import path from "path";
import fs from "fs";

function findPackageJsonDir(currentDir) {
  const packageJsonPath = path.join(currentDir, "package.json");
  if (fs.existsSync(packageJsonPath)) {
    return currentDir;
  }
  const parentDir = path.dirname(currentDir);
  if (parentDir === currentDir) {
    throw new Error("package.json not found");
  }
  return findPackageJsonDir(parentDir);
}

console.log(findPackageJsonDir(process.cwd()));
