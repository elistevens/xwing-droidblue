from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("_tensor_c_api", open('tensor_c_api.h').read(),
    libraries=[])   # or a list of libraries to link with
    # (more arguments like setup.py's Extension class:
    # include_dirs=[..], extra_objects=[..], and so on)

# ffibuilder.cdef("""
# typedef struct TF_Status TF_Status;
# """)
# ffibuilder.cdef("""
# typedef struct {
#   const void* data;
#   size_t length;
# } TF_Buffer;
# """)

#  void (*data_deallocator)(void* data, size_t length);

# ffibuilder.cdef("""
# extern TF_Buffer* TF_NewBufferFromString(const void* proto, size_t proto_len);
# """)

ffibuilder.cdef(open('tensor_c_api.cdef').read())
# ffibuilder.cdef("""     // some declarations from the man page
#     struct passwd {
#         char *pw_name;
#         ...;     // literally dot-dot-dot
#     };
#     struct passwd *getpwuid(int uid);
# """)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
