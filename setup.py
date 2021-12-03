from setuptools import setup

setups = ['setuptools']

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='CompressibleFlowFunctions',
    url='https://github.com/seanfcb/CompressibleFlowFunctions',
    author='Sean Connolly-Boutin',
    author_email='sean.connolly.boutin@gmail.com',
    # Needed to actually package something
    packages=['CompressibleFlowFunctions'],
    # Needed for dependencies
    setup_requires=setups,
    install_requires=['numpy','scipy'],
    # *strongly* suggested for sharing
    version='0.7',
    # The license can be anything you like
    #license='MIT',
    description='A package containing various functions in compressible flow',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
