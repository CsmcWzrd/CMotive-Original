// Package/plugin discovery, manifest, and loading scaffold.
// Package Foo::Bar; declares a namespace-like package.  Plugin Foo::Bar imports
// a package or .HMOT/.HMTV header.  The bootstrap compiler parses Plugin lines
// and the preprocessor resolves #include headers; the native package manager will
// use this contract for manifest and search-path based loading.
namespace cmotive::packages {
struct PackageFeatureMatrix {
    bool package_declaration = true;
    bool plugin_directive = true;
    bool hmot_hmtv_header_inputs = true;
    bool package_search_path = true;
    bool manifest_scaffold = true;
};
static constexpr PackageFeatureMatrix kPackageFeatureMatrix{};
} // namespace cmotive::packages
