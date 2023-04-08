import io
from trimesh import Trimesh
import numpy as np
from stl import mesh
import streamlit as st
import trimesh
from io import StringIO, BytesIO


def generate_mesh(height, radius):
    mesh = trimesh.creation.cylinder(radius=radius, height=height)
    return mesh


def download_mesh(mesh):
    buffer = BytesIO()
    mesh.export(buffer, file_type='stl')
    buffer.seek(0)
    st.download_button(
        label='Download STL',
        data=buffer,
        file_name='generated_mesh.stl',
        mime='application/octet-stream'
    )


def main():
    st.title("3D Cylinder Generator")
    st.write("This app generates a 3D cylinder mesh using the trimesh library")

    height = st.number_input("Enter the height of the cylinder:")
    radius = st.number_input("Enter the radius of the cylinder:")

    if st.button("Generate Mesh"):
        mesh = generate_mesh(height, radius)
        st.write(mesh)
        download_mesh(mesh)


if __name__ == "__main__":
    main()

# Define a function to get user input


def get_user_input():
    # Get dimensions from user
    x = st.slider('X Dimension', 1, 10, 5)
    y = st.slider('Y Dimension', 1, 10, 5)
    z = st.slider('Z Dimension', 1, 10, 5)

    # Get resolution from user
    resolution = st.slider('Resolution', 10, 100, 50)

    return x, y, z, resolution

# Define a function to generate a 3D mesh based on user input


def generate_mesh(x, y, z, resolution):
    # Define vertices
    vertices = np.array([
        [0, 0, 0],
        [x, 0, 0],
        [x, y, 0],
        [0, y, 0],
        [0, y, z],
        [x, y, z],
        [x, 0, z],
        [0, 0, z]
    ])

    # Define faces
    faces = np.array([
        [0, 3, 2],
        [0, 2, 1],
        [2, 3, 4],
        [2, 4, 5],
        [1, 2, 5],
        [1, 5, 6],
        [0, 7, 4],
        [0, 4, 3],
        [5, 4, 7],
        [5, 7, 6],
        [0, 1, 6],
        [0, 6, 7]
    ])

    # Create mesh
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            mesh_data.vectors[i][j] = vertices[f[j], :]

    # Export mesh to STL file
    mesh_data.save('output.stl')

    # Load STL file using Trimesh library
    tri_mesh = Trimesh('output.stl')

    # Simplify mesh using Quadric Edge Collapse Decimation algorithm
    tri_mesh_simplified = tri_mesh.simplify_quadric_decimation(resolution)

    # Return simplified mesh vertices and faces
    return tri_mesh_simplified.vertices, tri_mesh_simplified.faces

# Define main function


def main():
    # Set page title
    st.title('3D Mesh Generator')

    # Get user input
    x, y, z, resolution = get_user_input()

    # Generate mesh
    vertices, faces = generate_mesh(x, y, z, resolution)

    # Display 3D mesh
    st.write('3D Mesh:')
    st.write(vertices, faces)

    # Download STL file
    st.download_button(
        label='Download STL',
        data='output.stl',
        file_name='output.stl',
        mime='application/octet-stream'
    )


# Run main function
if __name__ == '__main__':
    main()


def main():
    st.title("3D Mesh Generator")

    # Sidebar options
    st.sidebar.header("Options")
    mesh_type = st.sidebar.selectbox("Select Mesh Type", ["Sphere", "Torus"])
    scale = st.sidebar.slider("Scale", 1, 10, 1)
    resolution = st.sidebar.slider("Resolution", 10, 100, 30)

    # Generate mesh based on selected type
    if mesh_type == "Sphere":
        mesh = trimesh.creation.icosphere(
            radius=scale, subdivisions=resolution)
    elif mesh_type == "Torus":
        mesh = trimesh.creation.torus(
            r1=scale, r2=0.4*scale, sections=resolution, subsections=resolution)

    # Preview the mesh
    mesh_preview = trimesh.Scene(mesh)
    preview_size = 800
    preview_image = mesh_preview.save_image(
        resolution=[preview_size, preview_size])
    st.image(preview_image)

    # Download mesh as STL file
    st.markdown("## Download Mesh")
    st.markdown("Click the button below to download the mesh as an STL file.")
    mesh_file = mesh.export(file_type="stl")
    mesh_bytes = io.BytesIO(mesh_file)
    st.download_button("Download STL", data=mesh_bytes,
                       file_name="mesh.stl", mime="application/octet-stream")


if __name__ == "__main__":
    main()
