from enum import Enum


class CompilerLevel(Enum):
    """The compiler level CFLAGS.
    See for more detail: https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html"""

    O0 = "O0"
    """Reduce compilation time and make debugging produce the expected results. This is the default. """
    O1 = "O1"
    """Optimize. Optimizing compilation takes somewhat more time, and a lot more memory for a large function.
    The compiler tries to reduce code size and execution time, without performing any optimizations that take a great deal of compilation time."""
    O2 = "O2"
    """Optimize even more. GCC performs nearly all supported optimizations that do not involve a space-speed tradeoff. As compared to -O, this option increases both compilation time and the performance of the generated code."""
    O3 = "O3"
    """Optimize yet more."""
    Os = "Os"
    """Optimize for size. Enables all O2 optimizations except those that often increase code size."""
    Ofast = "Ofast"
    """Disregard strict standards compliance. Enables all O3 optimizations. It also enables optimizations that are not valid for all standard-compliant programs."""
    Og = "Og"
    """Optimize debugging experience. Og should be the optimization level of choice for the standard edit-compile-debug cycle, offering a reasonable level of optimization while maintaining fast compilation and a good debugging experience.
    It is a better choice than O0 for producing debuggable code because some compiler passes that collect debug information are disabled at O0.
    Like O0, Og completely disables a number of optimization passes so that individual options controlling them have no effect.
    Otherwise Og enables all O1 optimization flags except for those that may interfere with debugging."""
    Oz = "Oz"
    """Optimize aggressively for size rather than speed. This may increase the number of instructions executed if those instructions require fewer bytes to encode. Oz behaves similarly to Os including enabling most O2 optimizations."""