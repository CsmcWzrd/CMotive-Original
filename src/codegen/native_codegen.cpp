// CMotive native codegen scaffold for x86, x86_64, ARM and ARM64.
// The executable bootstrap backend lowers CMotive AST to native C and invokes the
// platform compiler/linker to produce strip-compatible object/executable output.
namespace cmotive::codegen {
enum class TargetArch { Arm, Arm64, X86, X86_64, Native };
struct NativeCodegenFeatureMatrix {
    bool emits_native_objects = true;
    bool emits_native_executables = true;
    bool uses_platform_linker_path = true;
    bool keeps_strip_compatible_symbols = true;
    bool lowers_classes_to_c_structs = true;
    bool reserves_vtable_layout = true;
    bool lowers_new_delete_helpers = true;
    bool lowers_stdio_fluent_calls = true;
    bool lowers_rotate_shift_operators = true;
};
static constexpr NativeCodegenFeatureMatrix kNativeCodegenFeatureMatrix{};
} // namespace cmotive::codegen
