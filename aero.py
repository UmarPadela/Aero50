import matplotlib.pyplot as plt, mpld3
from xfoil import XFoil


def alpha_inv_analysis(airfoil, alpha_i, alpha_f, alpha_step, max_iter, id):
    """Inviscid analysis over range of angle of attacks."""
    # Initializes airfoil and assigns NACA 
    xf = XFoil()
    xf.naca(airfoil)
    xf.max_iter = max_iter
    # Collects values
    a, cl, cd, cm, cp = xf.aseq(alpha_i, alpha_f, alpha_step)
    x, cp_0 = xf.get_cp_distribution()
    # Plots all the data
    plot(a, cl, cd, cm, cp, x, cp_0, id)


def cl_inv_analysis(airfoil, cl_i, cl_f, cl_step, max_iter, id):
    """Inviscid analysis over range of angle of attacks."""
    # Initializes airfoil and assigns NACA 
    xf = XFoil()
    xf.naca(airfoil)
    xf.max_iter = max_iter
    # Collects values
    a, cl, cd, cm, cp = xf.cseq(cl_i, cl_f, cl_step)
    x, cp_0 = xf.get_cp_distribution()
    # Plots all the data
    plot(a, cl, cd, cm, cp, x, cp_0, id)


def alpha_visc_analysis(airfoil, alpha_i, alpha_f, alpha_step, re, mach, max_iter, id):
    """Viscous analysis over range of angle of attacks."""
    # Initializes airfoil and assigns NACA 
    xf = XFoil()
    xf.naca(airfoil)
    xf.max_iter = max_iter
    xf.Re = re
    xf.M = mach
    # Collects values
    a, cl, cd, cm, cp = xf.aseq(alpha_i, alpha_f, alpha_step)
    x, cp_0 = xf.get_cp_distribution()
    # Plots all the data
    plot(a, cl, cd, cm, cp, x, cp_0, id)
    
    

def cl_visc_analysis(airfoil, cl_i, cl_f, cl_step, re, mach, max_iter, id):
    """Viscous analysis over range of lift coefficients."""
    # Initializes airfoil and assigns NACA 
    xf = XFoil()
    xf.naca(airfoil)
    xf.max_iter = max_iter
    xf.Re = re
    xf.M = mach
    # Collects values
    a, cl, cd, cm, cp = xf.cseq(cl_i, cl_f, cl_step)
    x, cp_0 = xf.get_cp_distribution()
    # Plots all the data
    plot(a, cl, cd, cm, cp, x, cp_0, id)
    
    
    
    
def plot(a, cl, cd, cm, cp, x, cp_0, id):
    plot_lift_curve(a, cl, id)
    plot_drag_polar(cd, cl, id)
    plot_moment_curve(a, cm, id)
    plot_pressure_distribution(x, cp_0, id)
    plot_pressure_curve(a, cp, id)   


def plot_lift_curve(a, cl, id):
    """Plots lift curve and saves it."""
    file_path = f"./static/plots/{id}/lift_curve.png"
    fig, axes = plt.subplots()
    axes.plot(a, cl)
    axes.set_title ("Lift Curve")
    axes.set_xlabel("Angle of Attack (deg)")
    axes.set_ylabel("Coefficient of Lift")
    fig.savefig(file_path)
    

def plot_drag_polar(cd, cl, id):
    """Plots drag polar and saves it."""
    file_path = f"./static/plots/{id}/drag_polar.png"
    fig, axes = plt.subplots()
    axes.plot(cd, cl)
    axes.set_title ("Drag Polar")
    axes.set_xlabel("Coefficient of Drag")
    axes.set_ylabel("Coefficient of Lift")
    fig.savefig(file_path)

def plot_moment_curve(a, cm, id):
    """Plots moment curve and saves it."""
    file_path = f"./static/plots/{id}/moment_curve.png"
    fig, axes = plt.subplots()
    axes.plot(a, cm)
    axes.set_title ("Pitching Moment Curve")
    axes.set_xlabel("Angle of Attack (deg)")
    axes.set_ylabel("Pitching Moment")
    fig.savefig(file_path)

def plot_pressure_curve(a, cp, id):
    """Plots pressure curve and saves it."""
    file_path = f"./static/plots/{id}/pressure_curve.png"
    fig, axes = plt.subplots()
    axes.plot(a, cp)
    axes.set_title ("Minimum Pressure Curve")
    axes.set_xlabel("Angle of Attack (deg)")
    axes.set_ylabel("Minimum Coefficient of Pressure Along Airfoil")
    fig.savefig(file_path)
    

    
def plot_pressure_distribution(x, cp_0, id):
    """"Plots pressure distribution at last converged point and saves it."""
    file_path = f"./static/plots/{id}/pressure_distribution.png"
    fig, axes = plt.subplots()
    axes.plot(x, cp_0)
    axes.set_title ("Pressure Distribution at Last Converged Point")
    axes.set_xlabel("X-Coordinate of Airfoil")
    axes.set_ylabel("Coefficient of Pressure")
    fig.savefig(file_path)

    
    
