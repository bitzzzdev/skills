# Ecosystem search tips

Read only the section that matches the failing toolchain. These tell you where to look and what to put in the query; they are not fixes. Always confirm the answer against a page you actually opened.

## Contents
- JavaScript / TypeScript (npm, Vite, Next.js, webpack, tsc)
- Three.js / WebGL / GLSL
- Python
- Gradle, Fabric, and Minecraft mods
- Iris / OptiFine shaderpacks
- Android
- Rust and Go
- Git, CI, and Codespaces

## JavaScript / TypeScript
- Get versions from `package.json` and the lockfile; check the Node version too (`node -v`). Many errors are Node-version or peer-dependency mismatches.
- TypeScript errors have codes (`TS2307`, `TS2322`). Put the code and the TypeScript version in the query.
- "Cannot find module" / ESM-vs-CJS errors: search the package name plus "ESM" and its version; check the package's own README and `exports` field.
- Framework build failures (Vite, Next.js, webpack): look for the framework's official docs and its migration or upgrade guide for the installed major version, and its GitHub issues.
- Install failures (`ERESOLVE`, peer deps): read the full dependency chain in the output before searching; the conflicting pair of package names belongs in the query.
- Browser API questions: MDN is the primary reference.

## Three.js / WebGL / GLSL
- Three.js APIs change between releases. Find the installed version (`three` in `package.json`) and check the official docs and the migration guide for that version.
- Import path errors (`three/examples/jsm/...` vs `three/addons/...`) are usually version-related; search the release notes.
- Shader compile errors: the driver's error line numbers refer to the final assembled shader. Search with the GLSL version (`#version`, WebGL1 vs WebGL2) and the exact message.

## Python
- Note the Python version and package version (`pip show <pkg>`). Check the package's changelog for deprecations and removed APIs.
- For tracebacks, search the last exception line plus the library name, not the whole trace.
- Environment problems (wrong interpreter, missing wheel): check the package's install docs and its GitHub issues for the platform.

## Gradle, Fabric, and Minecraft mods
- Record the Minecraft version, Fabric Loader, Fabric API, Fabric Loom, Gradle, and Java versions. Most failures are version-combination problems.
- Use Fabric's official documentation and its developer tooling pages for the current Loom and mappings setup; Minecraft updates frequently change the build setup (mappings, Java version, Loom version).
- Gradle errors: search with the Gradle version and the Java version; Gradle's own docs have a compatibility matrix and upgrade guides.
- Mixin errors: include the target class, the Minecraft version, and the mappings in use.
- Don't rely on remembered class or method names; they differ by version and mappings. Confirm against current sources.

## Iris / OptiFine shaderpacks
- Shader program names, uniforms, and `shaders.properties` keys differ by Iris and Minecraft version. Use the Iris shader documentation (the IrisShaders/ShaderDoc repository on GitHub) and Iris release notes for the installed version.
- For GLSL compile errors reported in the Iris log, search the exact message with the `#version` used and the program name (`gbuffers_*`, `composite`, `final`, etc.).
- When the `iris-shaderpack-dev` skill is available, use it alongside this one for shader-specific work.

## Android
- Record Android Gradle Plugin (AGP), Gradle, Kotlin, compileSdk, and Java versions; AGP has a strict compatibility table with Gradle.
- Prefer developer.android.com docs and release notes for AGP and the specific AndroidX library version in use.
- For Jetpack Compose and AndroidX, search the library's release notes for the artifact version; behavior and APIs shift between versions.

## Rust and Go
- Rust compiler errors have codes (`E0308`). Search the code; the official error index explains it. Check the crate's docs.rs page for the version in `Cargo.toml`.
- Go: check the module version in `go.mod`, the package's pkg.go.dev page, and the Go release notes if the error appeared after a toolchain upgrade.

## Git, CI, and Codespaces
- For CI failures, read the failing job's log from the first error, and check whether the runner image or tool version changed recently (the action's releases page and the runner image's changelog).
- Codespaces: check the dev container configuration and the repository's `.devcontainer` files before searching; many failures come from image or feature version changes.
- Git errors: the official Git documentation is authoritative; search the exact message.
