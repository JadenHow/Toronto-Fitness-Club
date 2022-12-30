import React, { useState, useEffect } from 'react';
import algoliasearch from 'algoliasearch/lite';
import { InstantSearch, SearchBox, Hits, Highlight, Pagination, Configure } from 'react-instantsearch-hooks-web';
import "../StudioComponents/studio.css";
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ClassDetailComponents from '../../components/ClassComponents/ClassDetail'
import "./studiosearch.css";
import { Pagination as PaginationANTD } from 'antd';

const searchClient = algoliasearch('2SE5TN8IRT', 'aa72026cb29188c2018f9011071e18e5');

function StudioHit({ hit }) {
    const navigate = useNavigate();
    function handleClick() {navigate(`/studios/${hit.objectID}`)};

    return (
        <div className="s-border" style={{ cursor: 'pointer' }} onClick={handleClick}>
            <div className="s-content">
                <h2><Highlight attribute="name" hit={hit} /></h2>
                <h4>{hit.address}</h4>
                <h4>{hit.postal_code}</h4>
                <h4>{hit.phone_number}</h4>
            </div>
        </div>
    );
}

function AmenityHit({ hit }) {
    const split_studio = hit.studio.split("(")
    const navigate = useNavigate();
    function handleClick() { navigate(`/studios/${split_studio[1][0]}`) };

    return (
        <div className="s-border" style={{ cursor: 'pointer' }} onClick={handleClick}>
            <div className="s-content">
                <h2><Highlight attribute="type" hit={hit} /></h2>
                <h4>{hit.quantity}</h4>
                <h5>Click for more details</h5>
            </div>
        </div>
    );
}

const StudioSearch = () => {
    return (
        <InstantSearch searchClient={searchClient} indexName="backend_Studio">
            <Configure hitsPerPage={10} />
            <br />
            Search for Studios: <SearchBox />
            <Hits hitComponent={StudioHit} />
            <Pagination></Pagination>
        </InstantSearch>
    )
};

const AmenitiesSearch = () => {
    return (
        <InstantSearch searchClient={searchClient} indexName="backend_StudioAmenities">
            <Configure hitsPerPage={10} />
            <br />
            Search for Amenities: <SearchBox />
            <Hits hitComponent={AmenityHit} />
            <Pagination></Pagination>
        </InstantSearch>
    )
};

const ClassInstanceSearch = () => {
    const [posts, setPosts] = useState([])
    const [offset, setOffset] = useState(0);
    const [count, setCount] = useState(0);

    function handleChange(value) {
        setOffset((value - 1) * 10);
    };

    function class_search(search, start_date, end_date, start_time, end_time) {
        axios.get(`http://localhost:8000/classes/search/?q=${search}&start=${start_date}&end=${end_date}&starttime=${start_time}&endttime=${end_time}?limit=10&offset=${offset}`)
            .then(res => {
                setPosts(res.data.results)
                setCount(res.data.count)
            })
            .catch(err => {
                console.log(err)
            })
    };

    useEffect(() => {
        class_search(search, start_date, end_date, start_time, end_time);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [offset])

    const [searchData, setSearchData] = useState({
        search: '',
        start_date: '',
        end_date: '',
        start_time: '',
        end_time: '',
    });

    const { search, start_date, end_date, start_time, end_time } = searchData;

    const onChange = e => setSearchData({ ...searchData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();

        class_search(search, start_date, end_date, start_time, end_time);
    };
    return (
        <div>
            <div>
                <h1>Search for classes or coaches:</h1>
                <form onSubmit={e => onSubmit(e)}>
                    <div className='form-group'>
                        <input
                            className='search-bar'
                            type='search'
                            placeholder='Search'
                            name='search'
                            value={search}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='form-group'>
                        <input
                            className='search-control'
                            type='start_date'
                            placeholder='Start Date (optional) In this format: 2022-12-20'
                            name='start_date'
                            value={start_date}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='form-group'>
                        <input
                            className='search-control'
                            type='end_date'
                            placeholder='End date (optional) In this format: 2022-12-22'
                            name='end_date'
                            value={end_date}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='form-group'>
                        <input
                            className='search-control'
                            type='start_time'
                            placeholder='Start Time (optional) In this format: 01:55:00'
                            name='start_time'
                            value={start_time}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <div className='form-group'>
                        <input
                            className='search-control'
                            type='end_time'
                            placeholder='End Time (optional) In this format: 02:55:00'
                            name='end_time'
                            value={end_time}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <button className='btn btn-primary' type='submit'>Search</button>
                </form>
            </div>
            <div>
                {posts.map((posts, i) => (
                    <ClassDetailComponents key={i} pk={posts.objectID} name={posts.name} description={posts.description} coach={posts.coach} keywords={posts.keywords} capacity={posts.capacity} currently_enrolled={posts.currently_enrolled} class_date={posts.class_date} start_time={posts.start_time} end_time={posts.end_time} />
                ))}
            </div>
            <br />
            <PaginationANTD
                defaultCurrent={1}
                defaultPageSize={10} //default size of page
                onChange={handleChange}
                total={count} //total number of card data available
            />
        </div>
    )
};



const ClassStudioSearch = () => {

    const [posts, setPosts] = useState([])
    const current_url = window.location.pathname

    function class_studio_search(search, studio_id) {
        axios.get(`http://localhost:8000/studios/search/?q=${search}&studio=${studio_id}`)
            .then(res => {
                setPosts(res.data.results)
            })
            .catch(err => {
                console.log(err)
            })
    };

    const [searchData, setSearchData] = useState({
        search: '',
    });

    const { search } = searchData;

    const onChange = e => setSearchData({ ...searchData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();
        class_studio_search(search, current_url.split('/')[2]);
    };

    return (
        <div>
            <div>
                <h1>Search for classes or coaches:</h1>
                <form onSubmit={e => onSubmit(e)}>
                    <div className='form-group'>
                        <input
                            className='search-bar'
                            type='search'
                            placeholder='Search'
                            name='search'
                            value={search}
                            onChange={e => onChange(e)}
                        />
                    </div>
                    <button className='btn btn-primary' type='submit'>Search</button>
                </form>
            </div>
            <div>
                {posts.map((posts, i) => (
                    <ClassDetailComponents key={i} pk={posts.pk} name={posts.name} description={posts.description} coach={posts.coach} keywords={posts.keywords} capacity={posts.capacity} currently_enrolled={posts.currently_enrolled} class_date={posts.class_date} start_time={posts.start_time} end_time={posts.end_time} />
                ))}
            </div>
        </div>
    )
};

export { ClassStudioSearch, ClassInstanceSearch, StudioSearch, AmenitiesSearch };
